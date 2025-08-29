#!/usr/bin/env python3
"""
OpenAI Unified Agent Module

This module provides a unified agent class that can work with all supported
OpenAI models including GPT-4.1, GPT-4.1-mini, and GPT-4.1-nano.
"""

import json
import yaml
from pathlib import Path
from datetime import datetime
from typing import Optional, Generator, List, Dict, Any
from dataclasses import asdict

from config import AgentConfig, ModelRegistry
from utils import (
    DirectoryManager, LoggingManager, APIKeyManager, FileManager, 
    APIClient, ValidationUtils, ColorUtils
)


class UnifiedOpenAIAgent:
    """Unified OpenAI Chat Agent supporting multiple model variants"""
    
    def __init__(self, agent_id: str, model: str = "gpt-4.1"):
        """
        Initialize the unified agent
        
        Args:
            agent_id: Unique identifier for this agent instance
            model: OpenAI model to use (gpt-4.1, gpt-4.1-mini, gpt-4.1-nano)
        """
        # Validate inputs
        if not ValidationUtils.validate_agent_id(agent_id):
            raise ValueError(f"Invalid agent ID: {agent_id}")
        
        if not ModelRegistry.is_valid_model(model):
            raise ValueError(f"Unsupported model: {model}. Supported models: {ModelRegistry.list_models()}")
        
        self.agent_id = agent_id
        self.model = model
        
        # Setup directory structure
        self.base_dir = DirectoryManager.setup_agent_directories(agent_id)
        
        # Setup logging
        self.logger = LoggingManager.setup_logger(agent_id, self.base_dir)
        
        # Load or create configuration
        self.config = self._load_config()
        
        # Ensure model matches the specified one
        if self.config.model != model:
            self.config.model = model
            self._save_config()
        
        # Load conversation history
        self.messages = self._load_history()
        
        # Setup API key and client
        self.api_key = APIKeyManager.get_api_key(self.base_dir, model)
        self.api_client = APIClient(self.api_key, model, self.logger)
        
        model_display = ModelRegistry.get_model_display_name(model)
        self.logger.info(f"Initialized Unified OpenAI Agent: {agent_id} with model: {model_display}")
    
    def _load_config(self) -> AgentConfig:
        """Load agent configuration from config.yaml"""
        config_file = self.base_dir / "config.yaml"
        
        if config_file.exists():
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    config_data = yaml.safe_load(f)
                    return AgentConfig(**config_data)
            except Exception as e:
                self.logger.error(f"Error loading config: {e}")
                return ModelRegistry.get_default_config(self.model)
        else:
            config = ModelRegistry.get_default_config(self.model)
            self._save_config(config)
            return config
    
    def _save_config(self, config: Optional[AgentConfig] = None):
        """Save agent configuration to config.yaml"""
        if config is None:
            config = self.config
        
        config.updated_at = datetime.now().isoformat()
        config_file = self.base_dir / "config.yaml"
        
        try:
            with open(config_file, 'w', encoding='utf-8') as f:
                yaml.dump(asdict(config), f, default_flow_style=False, allow_unicode=True)
        except Exception as e:
            self.logger.error(f"Error saving config: {e}")
    
    def _load_history(self) -> List[Dict[str, Any]]:
        """Load conversation history from history.json"""
        history_file = self.base_dir / "history.json"
        
        if history_file.exists():
            try:
                with open(history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                self.logger.error(f"Error loading history: {e}")
                return []
        return []
    
    def _save_history(self):
        """Save conversation history to history.json with backup"""
        history_file = self.base_dir / "history.json"
        
        # Create backup if history exists
        if history_file.exists():
            FileManager.create_backup(self.base_dir, "history.json")
        
        try:
            with open(history_file, 'w', encoding='utf-8') as f:
                json.dump(self.messages, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"Error saving history: {e}")
    
    def add_message(self, role: str, content: str, metadata: Optional[Dict[str, Any]] = None):
        """Add a message to conversation history"""
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        }
        
        self.messages.append(message)
        
        # Truncate history if needed
        if len(self.messages) > self.config.max_history_size:
            removed = self.messages[:-self.config.max_history_size]
            self.messages = self.messages[-self.config.max_history_size:]
            self.logger.info(f"Truncated history: removed {len(removed)} old messages")
        
        self._save_history()
    
    def _build_api_payload(self, new_message: str, override_config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Build the API request payload based on model type"""
        # Process file inclusions
        processed_message = FileManager.process_file_inclusions(new_message, self.base_dir, self.logger)
        
        # Build messages array
        messages = []
        
        # Add system prompt if configured
        if self.config.system_prompt:
            system_message = {"role": "system", "content": self.config.system_prompt}
            
            # Use structured format for gpt-4.1-mini
            if self.model == "gpt-4.1-mini":
                system_message["content"] = [{"type": "text", "text": self.config.system_prompt}]
            
            messages.append(system_message)
        
        # Add conversation history
        for msg in self.messages:
            if msg["role"] in ["user", "assistant"]:
                message_content = {"role": msg["role"], "content": msg["content"]}
                
                # Use structured format for gpt-4.1-mini
                if self.model == "gpt-4.1-mini":
                    message_content["content"] = [{"type": "text", "text": msg["content"]}]
                
                messages.append(message_content)
        
        # Add new user message
        user_message = {"role": "user", "content": processed_message}
        
        # Use structured format for gpt-4.1-mini
        if self.model == "gpt-4.1-mini":
            user_message["content"] = [{"type": "text", "text": processed_message}]
        
        messages.append(user_message)
        
        # Apply config overrides
        config = asdict(self.config)
        if override_config:
            config.update(override_config)
        
        # Build payload based on model type
        payload = {
            "model": config["model"],
            "messages": messages,
            "temperature": config["temperature"],
            "top_p": config["top_p"],
            "frequency_penalty": config["frequency_penalty"],
            "presence_penalty": config["presence_penalty"],
        }
        
        # Add max_tokens (different parameter names for different models)
        if self.model == "gpt-4.1-mini":
            payload["max_completion_tokens"] = config["max_tokens"]
            payload["response_format"] = {"type": config["response_format"]}
        else:
            payload["max_tokens"] = config["max_tokens"]
        
        # Add streaming if enabled
        if config["stream"]:
            payload["stream"] = True
        
        return payload
    
    def call_api(self, new_message: str, override_config: Optional[Dict[str, Any]] = None) -> Generator[str, None, None]:
        """Call OpenAI API with the new message"""
        try:
            # Add user message to history
            self.add_message("user", new_message)
            
            # Build API payload
            payload = self._build_api_payload(new_message, override_config)
            
            self.logger.info(f"Making API call to {self.api_client.api_url}")
            self.logger.debug(f"Payload: {json.dumps(payload, indent=2)}")
            
            # Show model info to user
            model_display = ModelRegistry.get_model_display_name(self.model)
            timeout = ModelRegistry.get_model_timeout(self.model)
            
            print(ColorUtils.warning(f"🤖 Using {model_display} (timeout: {timeout//60}min {timeout%60}s)..."))
            
            # Make request
            response = self.api_client.make_request(payload)
            
            # Handle streaming vs non-streaming
            if payload.get("stream", True):
                assistant_message = ""
                for chunk in self.api_client.parse_streaming_response(response):
                    assistant_message += chunk
                    yield chunk
                
                # Add assistant message to history if we got content
                if assistant_message.strip():
                    self.add_message("assistant", assistant_message)
            else:
                result = self.api_client.parse_non_streaming_response(response)
                if result and result.strip():
                    self.add_message("assistant", result)
                yield result
                
        except Exception as e:
            error_msg = f"API call failed: {e}"
            self.logger.error(error_msg)
            yield error_msg
    
    def clear_history(self):
        """Clear conversation history"""
        FileManager.create_backup(self.base_dir, "history.json")
        self.messages.clear()
        self._save_history()
        self.logger.info("Conversation history cleared")
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get conversation statistics"""
        if not self.messages:
            return {
                "total_messages": 0,
                "user_messages": 0,
                "assistant_messages": 0,
                "total_characters": 0,
                "average_message_length": 0,
                "first_message": None,
                "last_message": None,
                "conversation_duration": None
            }
        
        user_msgs = [m for m in self.messages if m["role"] == "user"]
        assistant_msgs = [m for m in self.messages if m["role"] == "assistant"]
        
        total_chars = sum(len(m["content"]) for m in self.messages)
        avg_length = total_chars // len(self.messages) if self.messages else 0
        
        first_time = datetime.fromisoformat(self.messages[0]["timestamp"])
        last_time = datetime.fromisoformat(self.messages[-1]["timestamp"])
        duration = last_time - first_time
        
        return {
            "total_messages": len(self.messages),
            "user_messages": len(user_msgs),
            "assistant_messages": len(assistant_msgs),
            "total_characters": total_chars,
            "average_message_length": avg_length,
            "first_message": first_time.strftime("%Y-%m-%d %H:%M:%S"),
            "last_message": last_time.strftime("%Y-%m-%d %H:%M:%S"),
            "conversation_duration": str(duration).split('.')[0] if duration.total_seconds() > 0 else "0:00:00"
        }
    
    def search_history(self, term: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search conversation history for a term"""
        results = []
        term_lower = term.lower()
        
        for i, msg in enumerate(self.messages):
            if term_lower in msg["content"].lower():
                results.append({
                    "index": i,
                    "message": msg,
                    "preview": msg["content"][:100] + "..." if len(msg["content"]) > 100 else msg["content"]
                })
            
            if len(results) >= limit:
                break
        
        return results
    
    def list_files(self) -> List[str]:
        """List available files for inclusion"""
        return FileManager.list_available_files(self.base_dir)
    
    def update_config(self, **kwargs):
        """Update agent configuration"""
        config_dict = asdict(self.config)
        
        for key, value in kwargs.items():
            if key in config_dict:
                # Validate specific fields
                if key == "temperature" and not ValidationUtils.validate_temperature(value):
                    raise ValueError(f"Invalid temperature value: {value}")
                if key == "max_tokens" and not ValidationUtils.validate_max_tokens(value):
                    raise ValueError(f"Invalid max_tokens value: {value}")
                if key == "model" and not ModelRegistry.is_valid_model(value):
                    raise ValueError(f"Invalid model: {value}")
                
                setattr(self.config, key, value)
            else:
                raise ValueError(f"Unknown configuration key: {key}")
        
        self._save_config()
        self.logger.info(f"Configuration updated: {kwargs}")
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current model"""
        return ModelRegistry.get_model_info(self.model)
    
    def switch_model(self, new_model: str):
        """Switch to a different model"""
        if not ModelRegistry.is_valid_model(new_model):
            raise ValueError(f"Unsupported model: {new_model}")
        
        old_model = self.model
        self.model = new_model
        self.config.model = new_model
        
        # Update API client
        self.api_client = APIClient(self.api_key, new_model, self.logger)
        
        self._save_config()
        
        old_display = ModelRegistry.get_model_display_name(old_model)
        new_display = ModelRegistry.get_model_display_name(new_model)
        self.logger.info(f"Switched model from {old_display} to {new_display}")
    
    def validate_configuration(self) -> List[str]:
        """Validate current configuration and return any issues"""
        issues = []
        
        if not ValidationUtils.validate_temperature(self.config.temperature):
            issues.append(f"Invalid temperature: {self.config.temperature}")
        
        if not ValidationUtils.validate_max_tokens(self.config.max_tokens):
            issues.append(f"Invalid max_tokens: {self.config.max_tokens}")
        
        if not ModelRegistry.is_valid_model(self.config.model):
            issues.append(f"Invalid model: {self.config.model}")
        
        return issues


def list_agents() -> List[Dict[str, Any]]:
    """List all available agents"""
    agents_dir = Path("agents")
    agents = []
    
    if not agents_dir.exists():
        return agents
    
    for agent_dir in agents_dir.iterdir():
        if agent_dir.is_dir():
            agent_info = {
                "id": agent_dir.name,
                "path": str(agent_dir),
                "exists": True
            }
            
            # Load configuration info
            config_file = agent_dir / "config.yaml"
            if config_file.exists():
                try:
                    with open(config_file) as f:
                        config = yaml.safe_load(f)
                        agent_info["model"] = config.get("model", "gpt-4.1")
                        agent_info["created_at"] = config.get("created_at")
                        agent_info["updated_at"] = config.get("updated_at")
                except:
                    pass
            
            # Load history info
            history_file = agent_dir / "history.json"
            if history_file.exists():
                try:
                    with open(history_file) as f:
                        history = json.load(f)
                        agent_info["message_count"] = len(history)
                        agent_info["history_size"] = history_file.stat().st_size
                except:
                    agent_info["message_count"] = 0
                    agent_info["history_size"] = 0
            else:
                agent_info["message_count"] = 0
                agent_info["history_size"] = 0
            
            agents.append(agent_info)
    
    return sorted(agents, key=lambda x: x.get("updated_at", ""))


def show_agent_info(agent_id: str):
    """Display detailed agent information"""
    agent_dir = Path(f"agents/{agent_id}")
    
    if not agent_dir.exists():
        print(ColorUtils.error(f"Agent '{agent_id}' not found"))
        return
    
    print(f"\n{ColorUtils.info('='*50)}")
    print(f"Agent Information: {ColorUtils.warning(agent_id)}")
    print(f"{ColorUtils.info('='*50)}")
    
    # Load and display config
    config_file = agent_dir / "config.yaml"
    if config_file.exists():
        try:
            with open(config_file) as f:
                config = yaml.safe_load(f)
            
            model = config.get('model', 'gpt-4.1')
            model_display = ModelRegistry.get_model_display_name(model)
            
            print(f"\n{ColorUtils.success('Configuration:')}")
            print(f"  Model: {model} ({model_display})")
            print(f"  Temperature: {config.get('temperature', 1.0)}")
            print(f"  Max Tokens: {config.get('max_tokens', 32768)}")
            print(f"  Streaming: {config.get('stream', True)}")
            print(f"  Created: {config.get('created_at', 'Unknown')}")
            print(f"  Updated: {config.get('updated_at', 'Unknown')}")
            
        except Exception as e:
            print(ColorUtils.error(f"Error loading config: {e}"))
    
    # Display history stats
    history_file = agent_dir / "history.json"
    if history_file.exists():
        try:
            with open(history_file) as f:
                history = json.load(f)
            
            user_msgs = len([m for m in history if m.get("role") == "user"])
            assistant_msgs = len([m for m in history if m.get("role") == "assistant"])
            total_chars = sum(len(m.get("content", "")) for m in history)
            
            print(f"\n{ColorUtils.success('Conversation History:')}")
            print(f"  Total Messages: {len(history)}")
            print(f"  User Messages: {user_msgs}")
            print(f"  Assistant Messages: {assistant_msgs}")
            print(f"  Total Characters: {total_chars:,}")
            print(f"  File Size: {history_file.stat().st_size:,} bytes")
            
            if history:
                first_msg = datetime.fromisoformat(history[0]["timestamp"])
                last_msg = datetime.fromisoformat(history[-1]["timestamp"])
                print(f"  First Message: {first_msg.strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"  Last Message: {last_msg.strftime('%Y-%m-%d %H:%M:%S')}")
                
        except Exception as e:
            print(ColorUtils.error(f"Error loading history: {e}"))
    else:
        print(f"\n{ColorUtils.warning('No conversation history found')}")
    
    # Display directory structure
    print(f"\n{ColorUtils.success('Directory Structure:')}")
    for item in sorted(agent_dir.rglob("*")):
        if item.is_file():
            size = item.stat().st_size
            size_str = f"{size:,}" if size < 1024 else f"{size/1024:.1f}K"
            rel_path = item.relative_to(agent_dir)
            print(f"  {rel_path} ({size_str} bytes)")