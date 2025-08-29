#!/usr/bin/env python3
"""
OpenAI Agent Utilities Module

This module provides shared utility functions for file operations, logging,
API key management, and other common operations across all agents.
"""

import os
import sys
import json
import re
import logging
import shutil
import time
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any, List, Generator

import requests
from requests.exceptions import RequestException, HTTPError, Timeout

from config import ModelRegistry, CLI_COLORS, DEFAULT_SEARCH_PATHS

# Try to import colorama for cross-platform color support
try:
    from colorama import Fore, Style, init as colorama_init
    colorama_init(autoreset=True)
    HAS_COLORAMA = True
except ImportError:
    # Fallback if colorama is not available
    class Fore:
        RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = WHITE = RESET = ""
    
    class Style:
        BRIGHT = DIM = RESET_ALL = ""
    
    HAS_COLORAMA = False


class ColorUtils:
    """Utility class for handling colored terminal output"""
    
    @staticmethod
    def colorize(text: str, color: str) -> str:
        """Apply color to text if colorama is available"""
        if not HAS_COLORAMA:
            return text
        
        color_map = {
            'red': Fore.RED,
            'green': Fore.GREEN,
            'yellow': Fore.YELLOW,
            'blue': Fore.BLUE,
            'cyan': Fore.CYAN,
            'white': Fore.WHITE,
            'magenta': Fore.MAGENTA,
            'reset': Style.RESET_ALL
        }
        
        color_code = color_map.get(color.lower(), '')
        return f"{color_code}{text}{Style.RESET_ALL}" if color_code else text
    
    @staticmethod
    def success(text: str) -> str:
        """Apply success color (green)"""
        return ColorUtils.colorize(text, 'green')
    
    @staticmethod
    def error(text: str) -> str:
        """Apply error color (red)"""
        return ColorUtils.colorize(text, 'red')
    
    @staticmethod
    def warning(text: str) -> str:
        """Apply warning color (yellow)"""
        return ColorUtils.colorize(text, 'yellow')
    
    @staticmethod
    def info(text: str) -> str:
        """Apply info color (cyan)"""
        return ColorUtils.colorize(text, 'cyan')


class DirectoryManager:
    """Manages directory structure for agents"""
    
    @staticmethod
    def setup_agent_directories(agent_id: str) -> Path:
        """Create necessary directory structure for an agent"""
        base_dir = Path(f"agents/{agent_id}")
        directories = [
            base_dir,
            base_dir / "backups",
            base_dir / "logs",
            base_dir / "exports",
            base_dir / "uploads"
        ]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
        
        return base_dir


class LoggingManager:
    """Manages logging configuration for agents"""
    
    @staticmethod
    def setup_logger(agent_id: str, base_dir: Path, level: int = logging.INFO) -> logging.Logger:
        """Configure logging to file and console"""
        log_file = base_dir / "logs" / f"{datetime.now().strftime('%Y-%m-%d')}.log"
        
        # Create logger
        logger = logging.getLogger(f"OpenAIAgent_{agent_id}")
        logger.setLevel(level)
        
        # Remove existing handlers
        logger.handlers.clear()
        
        # File handler
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        
        # Console handler (only warnings and errors)
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter('%(levelname)s: %(message)s')
        console_handler.setFormatter(console_formatter)
        console_handler.setLevel(logging.WARNING)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger


class APIKeyManager:
    """Manages API key storage and retrieval"""
    
    @staticmethod
    def get_api_key(base_dir: Path, model: str) -> str:
        """Get API key from environment or secrets file, prompt if needed"""
        # First try environment variable
        api_key = os.getenv('OPENAI_API_KEY')
        if api_key:
            return api_key

        # Try secrets file
        secrets_file = base_dir / "secrets.json"
        if secrets_file.exists():
            try:
                with open(secrets_file, 'r') as f:
                    secrets = json.load(f)
                    keys = secrets.get('keys', {})
                    # Try model-specific key first, then default
                    api_key = keys.get(model) or keys.get('default')
                    if api_key:
                        return api_key
            except Exception:
                pass

        # Prompt user for API key
        model_display = ModelRegistry.get_model_display_name(model)
        print(ColorUtils.warning(f"API key not found for OpenAI {model_display} model."))
        print("You can set the OPENAI_API_KEY environment variable or enter it now.")
        
        api_key = input(ColorUtils.info(f"Enter API key for OpenAI {model_display}: ")).strip()
        
        if not api_key:
            raise ValueError("API key is required")

        # Save to secrets file
        APIKeyManager.save_api_key(base_dir, api_key, model)
        return api_key

    @staticmethod
    def save_api_key(base_dir: Path, api_key: str, model: str):
        """Save API key to secrets file"""
        secrets_file = base_dir / "secrets.json"
        
        secrets = {
            "provider": "openai",
            "keys": {
                "default": api_key,
                model: api_key
            }
        }

        try:
            with open(secrets_file, 'w') as f:
                json.dump(secrets, f, indent=2)

            # Add to .gitignore
            APIKeyManager._update_gitignore()
            
            masked_key = f"{api_key[:4]}...{api_key[-2:]}" if len(api_key) > 6 else "***"
            print(ColorUtils.success(f"API key saved ({masked_key})"))

        except Exception as e:
            print(ColorUtils.error(f"Warning: Could not save API key to file: {e}"))

    @staticmethod
    def _update_gitignore():
        """Add secrets.json to .gitignore if not already present"""
        gitignore_file = Path('.gitignore')
        gitignore_content = ""
        
        if gitignore_file.exists():
            gitignore_content = gitignore_file.read_text()

        if 'secrets.json' not in gitignore_content:
            with open(gitignore_file, 'a') as f:
                f.write('\n# API Keys\n**/secrets.json\nsecrets.json\n')


class FileManager:
    """Manages file operations including inclusion and backup"""
    
    @staticmethod
    def process_file_inclusions(content: str, base_dir: Path, logger: logging.Logger) -> str:
        """Replace {filename} patterns with file contents"""
        def replace_file(match):
            filename = match.group(1)
            return FileManager._include_file(filename, base_dir, logger)
        
        return re.sub(r'\{([^}]+)\}', replace_file, content)

    @staticmethod
    def _include_file(filename: str, base_dir: Path, logger: logging.Logger) -> str:
        """Include a single file's content"""
        # Search paths
        search_paths = [Path(p) for p in DEFAULT_SEARCH_PATHS] + [base_dir / 'uploads']
        
        for search_path in search_paths:
            file_path = search_path / filename
            if file_path.exists() and file_path.is_file():
                
                # Check if file is supported
                if not ModelRegistry.is_supported_file(file_path):
                    logger.warning(f"Unsupported file type: {filename}")
                    return f"[WARNING: Unsupported file type {filename}]"
                
                try:
                    # Check file size (limit to 2MB)
                    max_size = 2 * 1024 * 1024  # 2MB
                    if file_path.stat().st_size > max_size:
                        logger.error(f"File {filename} too large (>2MB)")
                        return f"[ERROR: File {filename} too large (max 2MB)]"
                    
                    # Try UTF-8 first
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            file_content = f.read()
                    except UnicodeDecodeError:
                        # Fallback to latin-1
                        with open(file_path, 'r', encoding='latin-1') as f:
                            file_content = f.read()
                    
                    # Add file info header
                    file_info = FileManager._get_file_header(filename, file_path.suffix)
                    full_content = file_info + file_content
                    
                    logger.info(f"Included file: {filename} ({len(file_content)} chars, {file_path.suffix})")
                    return full_content
                    
                except Exception as e:
                    logger.error(f"Error reading file {filename}: {e}")
                    return f"[ERROR: Could not read {filename}: {e}]"
        
        logger.warning(f"File not found: {filename}")
        return f"[ERROR: File {filename} not found]"

    @staticmethod
    def _get_file_header(filename: str, suffix: str) -> str:
        """Generate appropriate file header comment based on file type"""
        suffix = suffix.lower()
        
        if suffix in ['.py', '.r']:
            return f"# File: {filename} ({suffix})\n"
        elif suffix in ['.html', '.xml']:
            return f"<!-- File: {filename} ({suffix}) -->\n"
        elif suffix in ['.css', '.scss', '.sass']:
            return f"/* File: {filename} ({suffix}) */\n"
        elif suffix in ['.sql']:
            return f"-- File: {filename} ({suffix})\n"
        else:
            return f"// File: {filename} ({suffix})\n"

    @staticmethod
    def create_backup(base_dir: Path, filename: str = "history.json", max_backups: int = 10):
        """Create rolling backup of a file"""
        source_file = base_dir / filename
        backup_dir = base_dir / "backups"
        
        if not source_file.exists():
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = backup_dir / f"{filename.replace('.json', '')}_{timestamp}.json"
        
        try:
            shutil.copy2(source_file, backup_file)
            
            # Keep only last max_backups backups
            backup_pattern = f"{filename.replace('.json', '')}_*.json"
            backups = sorted(backup_dir.glob(backup_pattern))
            while len(backups) > max_backups:
                oldest = backups.pop(0)
                oldest.unlink()
                
        except Exception as e:
            logging.error(f"Error creating backup: {e}")

    @staticmethod
    def list_available_files(base_dir: Path) -> List[str]:
        """List available files for inclusion"""
        files = []
        search_paths = [Path(p) for p in DEFAULT_SEARCH_PATHS] + [base_dir / 'uploads']
        
        for search_path in search_paths:
            if search_path.exists():
                for file_path in search_path.rglob("*"):
                    if (file_path.is_file() and
                        not file_path.name.startswith('.') and
                        ModelRegistry.is_supported_file(file_path)):
                        
                        size = file_path.stat().st_size
                        size_str = f"{size:,} bytes" if size < 1024*1024 else f"{size/(1024*1024):.1f} MB"
                        files.append(f"{file_path} ({size_str}) [{file_path.suffix}]")
        
        return sorted(files)


class APIClient:
    """Handles OpenAI API requests with retries and error handling"""
    
    def __init__(self, api_key: str, model: str, logger: logging.Logger):
        self.api_key = api_key
        self.model = model
        self.logger = logger
        self.api_url = "https://api.openai.com/v1/chat/completions"
    
    def make_request(self, payload: Dict[str, Any]) -> requests.Response:
        """Make API request with retries and error handling"""
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        timeout = ModelRegistry.get_model_timeout(self.model)
        model_display = ModelRegistry.get_model_display_name(self.model)
        
        max_retries = 3
        base_delay = 1
        
        for attempt in range(max_retries):
            try:
                self.logger.info(f"Making API request to {model_display} (attempt {attempt + 1}/{max_retries}) with {timeout}s timeout...")
                
                response = requests.post(
                    self.api_url,
                    headers=headers,
                    json=payload,
                    stream=payload.get("stream", True),
                    timeout=timeout
                )
                
                if response.status_code == 200:
                    self.logger.info("API request successful")
                    return response
                elif response.status_code == 401:
                    raise ValueError("Invalid API key")
                elif response.status_code == 403:
                    raise ValueError("API access forbidden")
                elif response.status_code == 429:
                    # Rate limited - wait and retry
                    delay = base_delay * (2 ** attempt)
                    self.logger.warning(f"Rate limited, retrying in {delay}s...")
                    time.sleep(delay)
                    continue
                elif response.status_code >= 500:
                    # Server error - retry
                    delay = base_delay * (2 ** attempt)
                    self.logger.warning(f"Server error {response.status_code}, retrying in {delay}s...")
                    time.sleep(delay)
                    continue
                else:
                    response.raise_for_status()
                    
            except Timeout:
                self.logger.warning(f"Request timed out after {timeout}s (attempt {attempt + 1}/{max_retries})")
                if attempt == max_retries - 1:
                    raise Exception(f"Request timed out after {timeout}s.")
                delay = base_delay * (2 ** attempt)
                self.logger.warning(f"Retrying in {delay}s...")
                time.sleep(delay)
            except RequestException as e:
                if attempt == max_retries - 1:
                    raise
                delay = base_delay * (2 ** attempt)
                self.logger.warning(f"Request failed ({e}), retrying in {delay}s...")
                time.sleep(delay)
        
        raise Exception(f"Failed to complete API request after {max_retries} attempts")

    def parse_streaming_response(self, response: requests.Response) -> Generator[str, None, None]:
        """Parse streaming Server-Sent Events response"""
        assistant_message = ""
        
        try:
            for line in response.iter_lines(decode_unicode=True):
                if not line or line.strip() == "":
                    continue
                
                try:
                    # Handle Server-Sent Events format
                    if line.startswith("data: "):
                        data_str = line[5:].strip()
                        
                        if data_str == "[DONE]":
                            break
                        
                        data = json.loads(data_str)
                        
                        # Extract content from response
                        choices = data.get("choices", [])
                        if choices:
                            choice = choices[0]
                            delta = choice.get("delta", {})
                            content = delta.get("content", "")
                            
                            if content:
                                assistant_message += content
                                yield content
                            
                            # Check for completion
                            finish_reason = choice.get("finish_reason")
                            if finish_reason == "stop":
                                break
                                
                except json.JSONDecodeError as e:
                    self.logger.warning(f"Invalid JSON in stream: {e}")
                    continue
                except Exception as e:
                    self.logger.warning(f"Error processing stream line: {e}")
                    continue
                    
        except Exception as e:
            self.logger.error(f"Error parsing streaming response: {e}")
        
        return assistant_message

    def parse_non_streaming_response(self, response: requests.Response) -> str:
        """Parse non-streaming response from OpenAI chat completions API"""
        try:
            data = response.json()
            
            # Extract message content from response
            choices = data.get("choices", [])
            if choices:
                message = choices[0].get("message", {})
                
                # Handle both structured and simple content formats
                content = message.get("content", "")
                if isinstance(content, list) and content:
                    # Structured format
                    content = content[0].get("text", "")
                
                if content:
                    return content
            
            return "No response content received"
            
        except Exception as e:
            self.logger.error(f"Error parsing non-streaming response: {e}")
            return f"Error parsing response: {e}"


class ValidationUtils:
    """Utility functions for validation"""
    
    @staticmethod
    def validate_agent_id(agent_id: str) -> bool:
        """Validate agent ID format"""
        if not agent_id:
            return False
        
        # Allow alphanumeric, hyphens, and underscores
        return bool(re.match(r'^[a-zA-Z0-9_-]+$', agent_id))
    
    @staticmethod
    def validate_temperature(temperature: float) -> bool:
        """Validate temperature value"""
        return 0.0 <= temperature <= 2.0
    
    @staticmethod
    def validate_max_tokens(max_tokens: Optional[int]) -> bool:
        """Validate max tokens value"""
        if max_tokens is None:
            return True
        return isinstance(max_tokens, int) and max_tokens > 0


def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format"""
    if size_bytes < 1024:
        return f"{size_bytes} bytes"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.1f} MB"


def format_duration(seconds: float) -> str:
    """Format duration in human readable format"""
    if seconds < 60:
        return f"{seconds:.0f}s"
    elif seconds < 3600:
        minutes = seconds // 60
        remaining_seconds = seconds % 60
        return f"{minutes:.0f}m {remaining_seconds:.0f}s"
    else:
        hours = seconds // 3600
        remaining_minutes = (seconds % 3600) // 60
        return f"{hours:.0f}h {remaining_minutes:.0f}m"