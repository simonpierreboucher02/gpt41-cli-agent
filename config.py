#!/usr/bin/env python3
"""
OpenAI Agent Configuration Module

This module provides configuration management for all supported OpenAI models
including GPT-4.1, GPT-4.1-mini, and GPT-4.1-nano variants.
"""

from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any
from datetime import datetime


@dataclass
class AgentConfig:
    """Unified configuration settings for OpenAI Chat Agents"""
    model: str = "gpt-4.1"
    temperature: float = 1.0
    max_tokens: Optional[int] = 32768
    max_history_size: int = 1000
    stream: bool = True
    system_prompt: Optional[str] = None
    response_format: str = "text"
    top_p: float = 1.0
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0
    created_at: str = ""
    updated_at: str = ""

    def __post_init__(self):
        """Initialize timestamps"""
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()


class ModelRegistry:
    """Registry of supported OpenAI models with their configurations"""
    
    SUPPORTED_MODELS = {
        "gpt-4.1": {
            "name": "GPT-4.1",
            "description": "Advanced GPT-4.1 model with comprehensive capabilities",
            "timeout": 300,  # 5 minutes
            "max_tokens": 32768,
            "api_format": "standard",
            "supports_streaming": True,
            "supports_vision": False,
            "cost_tier": "premium"
        },
        "gpt-4.1-mini": {
            "name": "GPT-4.1 Mini",
            "description": "Compact GPT-4.1-mini model balancing performance and efficiency",
            "timeout": 180,  # 3 minutes
            "max_tokens": 32768,
            "api_format": "structured",
            "supports_streaming": True,
            "supports_vision": False,
            "cost_tier": "standard"
        },
        "gpt-4.1-nano": {
            "name": "GPT-4.1 Nano",
            "description": "Lightweight GPT-4.1 model optimized for speed",
            "timeout": 120,  # 2 minutes
            "max_tokens": 32768,
            "api_format": "standard",
            "supports_streaming": True,
            "supports_vision": False,
            "cost_tier": "economy"
        }
    }

    # Programming and common file extensions supported for file inclusion
    SUPPORTED_EXTENSIONS = {
        # Programming languages
        '.py', '.r', '.js', '.ts', '.jsx', '.tsx', '.java', '.c', '.cpp', '.cc', '.cxx',
        '.h', '.hpp', '.cs', '.php', '.rb', '.go', '.rs', '.swift', '.kt', '.scala',
        '.clj', '.hs', '.ml', '.fs', '.vb', '.pl', '.pm', '.sh', '.bash', '.zsh', '.fish',
        '.ps1', '.bat', '.cmd', '.sql', '.html', '.htm', '.css', '.scss', '.sass', '.less',
        '.xml', '.xsl', '.xslt', '.json', '.yaml', '.yml', '.toml', '.ini', '.cfg', '.conf',
        '.properties', '.env', '.dockerfile', '.docker', '.makefile', '.cmake', '.gradle',
        '.sbt', '.pom', '.lock', '.mod', '.sum',

        # Data and markup
        '.md', '.markdown', '.rst', '.tex', '.latex', '.csv', '.tsv', '.jsonl', '.ndjson',
        '.svg', '.rss', '.atom', '.plist',

        # Configuration and infrastructure
        '.tf', '.tfvars', '.hcl', '.nomad', '.consul', '.vault', '.k8s', '.kubectl',
        '.helm', '.kustomize', '.ansible', '.inventory', '.playbook',

        # Documentation and text
        '.txt', '.log', '.out', '.err', '.trace', '.debug', '.info', '.warn', '.error',
        '.readme', '.license', '.changelog', '.authors', '.contributors', '.todo',

        # Notebooks and scripts
        '.ipynb', '.rmd', '.qmd', '.jl', '.m', '.octave', '.R', '.Rmd',

        # Web and API
        '.graphql', '.gql', '.rest', '.http', '.api', '.postman', '.insomnia',

        # Other useful formats
        '.editorconfig', '.gitignore', '.gitattributes', '.dockerignore', '.eslintrc',
        '.prettierrc', '.babelrc', '.webpack', '.rollup', '.vite', '.parcel'
    }

    @classmethod
    def get_model_info(cls, model: str) -> Dict[str, Any]:
        """Get information about a specific model"""
        return cls.SUPPORTED_MODELS.get(model, {})

    @classmethod
    def get_model_timeout(cls, model: str) -> int:
        """Get timeout for a specific model"""
        return cls.get_model_info(model).get('timeout', 120)

    @classmethod
    def get_model_display_name(cls, model: str) -> str:
        """Get display name for a specific model"""
        return cls.get_model_info(model).get('name', model)

    @classmethod
    def is_valid_model(cls, model: str) -> bool:
        """Check if model is supported"""
        return model in cls.SUPPORTED_MODELS

    @classmethod
    def list_models(cls) -> list:
        """Get list of all supported models"""
        return list(cls.SUPPORTED_MODELS.keys())

    @classmethod
    def get_default_config(cls, model: str) -> AgentConfig:
        """Get default configuration for a specific model"""
        if not cls.is_valid_model(model):
            model = "gpt-4.1"
        
        model_info = cls.get_model_info(model)
        return AgentConfig(
            model=model,
            max_tokens=model_info.get('max_tokens', 32768),
        )

    @classmethod
    def is_supported_file(cls, file_path) -> bool:
        """Check if file extension is supported for inclusion"""
        from pathlib import Path
        
        if hasattr(file_path, 'suffix'):
            path_obj = file_path
        else:
            path_obj = Path(file_path)
        
        if path_obj.suffix.lower() in cls.SUPPORTED_EXTENSIONS:
            return True

        # Check for files without extensions but with known names
        known_files = {
            'makefile', 'dockerfile', 'rakefile', 'gemfile', 'podfile',
            'readme', 'license', 'changelog', 'authors', 'contributors',
            'todo', 'manifest', 'requirements', 'pipfile', 'poetry'
        }

        return path_obj.name.lower() in known_files


# Default search paths for file inclusion
DEFAULT_SEARCH_PATHS = [
    '.',
    'src', 'lib',
    'scripts', 'data',
    'documents', 'files',
    'config', 'configs'
]

# Export format configurations
EXPORT_FORMATS = {
    'json': {
        'extension': '.json',
        'content_type': 'application/json',
        'description': 'JSON format with full metadata'
    },
    'txt': {
        'extension': '.txt',
        'content_type': 'text/plain',
        'description': 'Plain text format'
    },
    'md': {
        'extension': '.md',
        'content_type': 'text/markdown',
        'description': 'Markdown format'
    },
    'html': {
        'extension': '.html',
        'content_type': 'text/html',
        'description': 'HTML format with styling'
    }
}

# CLI Color scheme
CLI_COLORS = {
    'primary': '\033[94m',      # Blue
    'success': '\033[92m',      # Green
    'warning': '\033[93m',      # Yellow
    'error': '\033[91m',        # Red
    'info': '\033[96m',         # Cyan
    'reset': '\033[0m',         # Reset
    'bold': '\033[1m',          # Bold
    'dim': '\033[2m'            # Dim
}