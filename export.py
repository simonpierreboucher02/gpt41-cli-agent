#!/usr/bin/env python3
"""
OpenAI Agent Export Module

This module provides comprehensive export functionality for conversations
in multiple formats including JSON, TXT, Markdown, and HTML with enhanced styling.
"""

import json
import html
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List
from dataclasses import asdict

from config import ModelRegistry, EXPORT_FORMATS
from utils import ColorUtils


class ConversationExporter:
    """Handles exporting conversations to various formats"""
    
    def __init__(self, agent_id: str, base_dir: Path, config: Any, messages: List[Dict[str, Any]]):
        self.agent_id = agent_id
        self.base_dir = base_dir
        self.config = config
        self.messages = messages
        self.export_dir = base_dir / "exports"
        
        # Ensure export directory exists
        self.export_dir.mkdir(exist_ok=True)
    
    def export_conversation(self, format_type: str) -> str:
        """Export conversation to specified format"""
        if format_type not in EXPORT_FORMATS:
            raise ValueError(f"Unsupported export format: {format_type}. Supported: {list(EXPORT_FORMATS.keys())}")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        extension = EXPORT_FORMATS[format_type]['extension']
        filename = f"conversation_{timestamp}{extension}"
        filepath = self.export_dir / filename
        
        # Route to appropriate export method
        export_methods = {
            'json': self._export_json,
            'txt': self._export_txt,
            'md': self._export_markdown,
            'html': self._export_html
        }
        
        export_methods[format_type](filepath)
        return str(filepath)
    
    def _export_json(self, filepath: Path):
        """Export conversation as JSON with full metadata"""
        stats = self._calculate_statistics()
        model_display = ModelRegistry.get_model_display_name(self.config.model)
        
        export_data = {
            "agent_id": self.agent_id,
            "exported_at": datetime.now().isoformat(),
            "model": {
                "name": self.config.model,
                "display_name": model_display,
                "info": ModelRegistry.get_model_info(self.config.model)
            },
            "config": asdict(self.config),
            "messages": self.messages,
            "statistics": stats,
            "export_info": {
                "format": "json",
                "version": "1.0",
                "total_messages": len(self.messages),
                "file_size_bytes": 0  # Will be calculated after writing
            }
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        # Update file size in metadata (for future reference)
        export_data["export_info"]["file_size_bytes"] = filepath.stat().st_size
    
    def _export_txt(self, filepath: Path):
        """Export conversation as plain text"""
        model_display = ModelRegistry.get_model_display_name(self.config.model)
        stats = self._calculate_statistics()
        
        with open(filepath, 'w', encoding='utf-8') as f:
            # Header
            f.write("OpenAI Unified Agent Conversation Export\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Agent ID: {self.agent_id}\n")
            f.write(f"Model: {self.config.model} ({model_display})\n")
            f.write(f"Export Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Messages: {stats['total_messages']}\n")
            f.write(f"Conversation Duration: {stats['conversation_duration']}\n")
            f.write("\n" + "=" * 50 + "\n\n")
            
            # Configuration
            f.write("CONFIGURATION:\n")
            f.write("-" * 20 + "\n")
            config_dict = asdict(self.config)
            for key, value in config_dict.items():
                if key not in ['created_at', 'updated_at']:
                    f.write(f"{key.replace('_', ' ').title()}: {value}\n")
            f.write("\n")
            
            # Statistics
            f.write("STATISTICS:\n")
            f.write("-" * 20 + "\n")
            for key, value in stats.items():
                if value is not None:
                    display_key = key.replace('_', ' ').title()
                    f.write(f"{display_key}: {value}\n")
            f.write("\n" + "=" * 50 + "\n\n")
            
            # Messages
            f.write("CONVERSATION:\n")
            f.write("-" * 20 + "\n\n")
            
            for i, msg in enumerate(self.messages, 1):
                timestamp = datetime.fromisoformat(msg["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")
                role = msg["role"].upper()
                content = msg["content"]
                
                f.write(f"[{i:03d}] [{timestamp}] {role}:\n")
                f.write("-" * 40 + "\n")
                f.write(f"{content}\n\n")
    
    def _export_markdown(self, filepath: Path):
        """Export conversation as Markdown"""
        model_display = ModelRegistry.get_model_display_name(self.config.model)
        stats = self._calculate_statistics()
        
        with open(filepath, 'w', encoding='utf-8') as f:
            # Header
            f.write(f"# 🤖 OpenAI {model_display} Conversation\n\n")
            f.write(f"**Agent ID:** `{self.agent_id}`  \n")
            f.write(f"**Model:** `{self.config.model}`  \n")
            f.write(f"**Export Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  \n")
            f.write(f"**Total Messages:** {stats['total_messages']}  \n\n")
            
            # Model Information
            model_info = ModelRegistry.get_model_info(self.config.model)
            if model_info:
                f.write("## 📊 Model Information\n\n")
                f.write(f"- **Name:** {model_info.get('name', 'Unknown')}\n")
                f.write(f"- **Description:** {model_info.get('description', 'No description')}\n")
                f.write(f"- **Timeout:** {model_info.get('timeout', 'Unknown')}s\n")
                f.write(f"- **Max Tokens:** {model_info.get('max_tokens', 'Unknown')}\n")
                f.write(f"- **Cost Tier:** {model_info.get('cost_tier', 'Unknown').title()}\n\n")
            
            # Configuration
            f.write("## ⚙️ Configuration\n\n")
            config_dict = asdict(self.config)
            for key, value in config_dict.items():
                if key not in ['created_at', 'updated_at'] and value is not None:
                    display_key = key.replace('_', ' ').title()
                    f.write(f"- **{display_key}:** `{value}`\n")
            f.write("\n")
            
            # Statistics
            f.write("## 📈 Statistics\n\n")
            f.write("| Metric | Value |\n")
            f.write("|--------|-------|\n")
            for key, value in stats.items():
                if value is not None:
                    display_key = key.replace('_', ' ').title()
                    if isinstance(value, int) and key != 'conversation_duration':
                        f.write(f"| {display_key} | {value:,} |\n")
                    else:
                        f.write(f"| {display_key} | {value} |\n")
            f.write("\n")
            
            # Conversation
            f.write("## 💬 Conversation\n\n")
            
            for i, msg in enumerate(self.messages, 1):
                timestamp = datetime.fromisoformat(msg["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")
                role = msg["role"]
                content = msg["content"]
                
                # Role emoji and styling
                if role == "user":
                    role_emoji = "👤"
                    role_display = "User"
                elif role == "assistant":
                    role_emoji = "🤖"
                    role_display = "Assistant"
                else:
                    role_emoji = "ℹ️"
                    role_display = role.title()
                
                f.write(f"### {role_emoji} {role_display} - Message {i}\n")
                f.write(f"*{timestamp}*\n\n")
                
                # Format content - handle code blocks properly
                formatted_content = self._format_markdown_content(content)
                f.write(f"{formatted_content}\n\n")
                f.write("---\n\n")
    
    def _export_html(self, filepath: Path):
        """Export conversation as HTML with modern styling"""
        model_display = ModelRegistry.get_model_display_name(self.config.model)
        stats = self._calculate_statistics()
        model_info = ModelRegistry.get_model_info(self.config.model)
        
        # Modern HTML template with enhanced styling
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🤖 OpenAI {model_display} Conversation - {self.agent_id}</title>
    <style>
        :root {{
            --primary-color: #2563eb;
            --secondary-color: #f1f5f9;
            --success-color: #10b981;
            --warning-color: #f59e0b;
            --error-color: #ef4444;
            --text-color: #1e293b;
            --text-secondary: #64748b;
            --border-color: #e2e8f0;
            --user-bg: linear-gradient(135deg, #3b82f6, #1d4ed8);
            --assistant-bg: linear-gradient(135deg, #10b981, #059669);
            --code-bg: #f8fafc;
            --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            --shadow-lg: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', sans-serif;
            line-height: 1.6;
            color: var(--text-color);
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 1rem;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 1rem;
            box-shadow: var(--shadow-lg);
            overflow: hidden;
        }}

        .header {{
            background: var(--primary-color);
            color: white;
            padding: 2rem;
            text-align: center;
            position: relative;
        }}

        .header::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="20" cy="20" r="2" fill="rgba(255,255,255,0.1)"/><circle cx="80" cy="40" r="1.5" fill="rgba(255,255,255,0.1)"/><circle cx="40" cy="80" r="1" fill="rgba(255,255,255,0.1)"/></svg>');
            opacity: 0.3;
        }}

        .header-content {{
            position: relative;
            z-index: 1;
        }}

        .header h1 {{
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
            font-weight: 700;
        }}

        .header-subtitle {{
            font-size: 1.1rem;
            opacity: 0.9;
            margin-bottom: 1.5rem;
        }}

        .header-info {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            font-size: 0.9rem;
        }}

        .header-info-item {{
            background: rgba(255, 255, 255, 0.1);
            padding: 0.75rem 1rem;
            border-radius: 0.5rem;
            backdrop-filter: blur(10px);
        }}

        .model-info {{
            background: var(--secondary-color);
            padding: 2rem;
            border-bottom: 1px solid var(--border-color);
        }}

        .model-info h2 {{
            margin-bottom: 1rem;
            color: var(--primary-color);
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}

        .info-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
        }}

        .info-card {{
            background: white;
            padding: 1.5rem;
            border-radius: 0.75rem;
            box-shadow: var(--shadow);
            border-left: 4px solid var(--primary-color);
        }}

        .info-card h3 {{
            font-size: 0.9rem;
            font-weight: 600;
            color: var(--text-secondary);
            margin-bottom: 0.5rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .info-card-value {{
            font-size: 1.25rem;
            font-weight: 700;
            color: var(--primary-color);
        }}

        .stats {{
            background: var(--secondary-color);
            padding: 2rem;
            border-bottom: 1px solid var(--border-color);
        }}

        .stats h2 {{
            margin-bottom: 1.5rem;
            color: var(--primary-color);
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}

        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 1rem;
        }}

        .stat-card {{
            background: white;
            padding: 1.5rem;
            border-radius: 0.75rem;
            text-align: center;
            box-shadow: var(--shadow);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }}

        .stat-card:hover {{
            transform: translateY(-2px);
            box-shadow: var(--shadow-lg);
        }}

        .stat-value {{
            font-size: 2rem;
            font-weight: 800;
            color: var(--primary-color);
            margin-bottom: 0.25rem;
        }}

        .stat-label {{
            font-size: 0.8rem;
            color: var(--text-secondary);
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .messages {{
            padding: 2rem;
            background: #fafbfc;
        }}

        .messages h2 {{
            margin-bottom: 2rem;
            color: var(--primary-color);
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}

        .message {{
            margin-bottom: 2rem;
            display: flex;
            align-items: flex-start;
            gap: 1rem;
            animation: fadeIn 0.3s ease-in;
        }}

        .message.user {{
            flex-direction: row-reverse;
        }}

        .message-avatar {{
            width: 3rem;
            height: 3rem;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.2rem;
            font-weight: bold;
            color: white;
            flex-shrink: 0;
            box-shadow: var(--shadow);
        }}

        .message.user .message-avatar {{
            background: var(--user-bg);
        }}

        .message.assistant .message-avatar {{
            background: var(--assistant-bg);
        }}

        .message-content {{
            flex: 1;
            max-width: 70%;
        }}

        .message-bubble {{
            background: white;
            padding: 1.5rem;
            border-radius: 1rem;
            box-shadow: var(--shadow);
            position: relative;
        }}

        .message.user .message-bubble {{
            background: linear-gradient(135deg, #eff6ff, #dbeafe);
            border: 1px solid #bfdbfe;
        }}

        .message.assistant .message-bubble {{
            background: linear-gradient(135deg, #f0fdf4, #dcfce7);
            border: 1px solid #bbf7d0;
        }}

        .message-bubble::before {{
            content: '';
            position: absolute;
            top: 1rem;
            width: 0;
            height: 0;
            border: 8px solid transparent;
        }}

        .message.user .message-bubble::before {{
            right: -15px;
            border-left-color: #dbeafe;
        }}

        .message.assistant .message-bubble::before {{
            left: -15px;
            border-right-color: #dcfce7;
        }}

        .message-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 1px solid var(--border-color);
        }}

        .message-role {{
            font-weight: 600;
            text-transform: capitalize;
            font-size: 0.9rem;
        }}

        .message.user .message-role {{
            color: #1d4ed8;
        }}

        .message.assistant .message-role {{
            color: #059669;
        }}

        .message-time {{
            font-size: 0.8rem;
            color: var(--text-secondary);
        }}

        .message-text {{
            white-space: pre-wrap;
            word-wrap: break-word;
            line-height: 1.7;
        }}

        .code-block {{
            background: var(--code-bg);
            border: 1px solid var(--border-color);
            border-radius: 0.5rem;
            padding: 1rem;
            margin: 1rem 0;
            overflow-x: auto;
            font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
            font-size: 0.9rem;
            line-height: 1.5;
        }}

        .footer {{
            background: var(--secondary-color);
            padding: 1.5rem 2rem;
            text-align: center;
            font-size: 0.9rem;
            color: var(--text-secondary);
            border-top: 1px solid var(--border-color);
        }}

        .footer-links {{
            margin-top: 0.5rem;
        }}

        .footer-links a {{
            color: var(--primary-color);
            text-decoration: none;
            margin: 0 0.5rem;
        }}

        .footer-links a:hover {{
            text-decoration: underline;
        }}

        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        @media (max-width: 768px) {{
            body {{
                padding: 0.5rem;
            }}

            .header {{
                padding: 1.5rem 1rem;
            }}

            .header h1 {{
                font-size: 1.75rem;
            }}

            .header-info {{
                grid-template-columns: 1fr;
            }}

            .model-info, .stats, .messages {{
                padding: 1.5rem 1rem;
            }}

            .info-grid, .stats-grid {{
                grid-template-columns: 1fr;
            }}

            .message-content {{
                max-width: 85%;
            }}

            .message-bubble {{
                padding: 1rem;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="header-content">
                <h1>🤖 OpenAI {model_display}</h1>
                <p class="header-subtitle">Conversation Export</p>
                <div class="header-info">
                    <div class="header-info-item">
                        <strong>Agent ID:</strong> {self.agent_id}
                    </div>
                    <div class="header-info-item">
                        <strong>Model:</strong> {self.config.model}
                    </div>
                    <div class="header-info-item">
                        <strong>Export Date:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                    </div>
                    <div class="header-info-item">
                        <strong>Temperature:</strong> {self.config.temperature}
                    </div>
                </div>
            </div>
        </div>"""
        
        # Model Information Section
        if model_info:
            html_content += f"""
        <div class="model-info">
            <h2>📊 Model Information</h2>
            <div class="info-grid">
                <div class="info-card">
                    <h3>Model Name</h3>
                    <div class="info-card-value">{model_info.get('name', 'Unknown')}</div>
                </div>
                <div class="info-card">
                    <h3>Description</h3>
                    <div class="info-card-value" style="font-size: 0.9rem; line-height: 1.4;">{model_info.get('description', 'No description available')}</div>
                </div>
                <div class="info-card">
                    <h3>Timeout</h3>
                    <div class="info-card-value">{model_info.get('timeout', 'Unknown')}s</div>
                </div>
                <div class="info-card">
                    <h3>Cost Tier</h3>
                    <div class="info-card-value">{model_info.get('cost_tier', 'Unknown').title()}</div>
                </div>
            </div>
        </div>"""
        
        # Statistics Section
        html_content += f"""
        <div class="stats">
            <h2>📈 Conversation Statistics</h2>
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-value">{stats['total_messages']}</div>
                    <div class="stat-label">Total Messages</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{stats['user_messages']}</div>
                    <div class="stat-label">User Messages</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{stats['assistant_messages']}</div>
                    <div class="stat-label">AI Messages</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{stats['total_characters']:,}</div>
                    <div class="stat-label">Total Characters</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{stats['average_message_length']:,}</div>
                    <div class="stat-label">Avg Length</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{stats.get('conversation_duration', 'N/A')}</div>
                    <div class="stat-label">Duration</div>
                </div>
            </div>
        </div>"""
        
        # Messages Section
        html_content += """
        <div class="messages">
            <h2>💬 Conversation</h2>"""
        
        for i, msg in enumerate(self.messages, 1):
            timestamp = datetime.fromisoformat(msg["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")
            role = msg["role"]
            content = msg["content"]
            
            # Escape HTML and format content
            content_escaped = html.escape(content)
            content_formatted = self._format_html_content(content_escaped)
            
            avatar_text = "U" if role == "user" else "AI"
            role_display = "User" if role == "user" else "Assistant"
            
            html_content += f"""
            <div class="message {role}">
                <div class="message-avatar">{avatar_text}</div>
                <div class="message-content">
                    <div class="message-bubble">
                        <div class="message-header">
                            <span class="message-role">{role_display}</span>
                            <span class="message-time">{timestamp}</span>
                        </div>
                        <div class="message-text">{content_formatted}</div>
                    </div>
                </div>
            </div>"""
        
        # Footer
        html_content += f"""
        </div>
        
        <div class="footer">
            <p>Generated by OpenAI Unified Agent • Agent ID: {self.agent_id} • {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <div class="footer-links">
                <span>Model: {model_display}</span>
                <span>•</span>
                <span>Messages: {len(self.messages)}</span>
                <span>•</span>
                <span>Export Format: HTML</span>
            </div>
        </div>
    </div>
</body>
</html>"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
    
    def _calculate_statistics(self) -> Dict[str, Any]:
        """Calculate conversation statistics"""
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
    
    def _format_markdown_content(self, content: str) -> str:
        """Format content for Markdown export"""
        # Handle existing code blocks (don't double-wrap)
        if '```' in content:
            return content
        
        # Simple detection of code-like content
        lines = content.split('\n')
        formatted_lines = []
        in_code_block = False
        
        for line in lines:
            # Detect potential code lines
            if (line.strip().startswith(('def ', 'class ', 'import ', 'from ', '>', '#', '//', '--')) or
                '=' in line and any(keyword in line for keyword in ['function', 'const', 'let', 'var'])):
                if not in_code_block:
                    formatted_lines.append('```')
                    in_code_block = True
            elif in_code_block and line.strip() == '':
                pass  # Keep empty lines in code blocks
            elif in_code_block and not any(char in line for char in '(){}[];'):
                formatted_lines.append('```')
                in_code_block = False
            
            formatted_lines.append(line)
        
        if in_code_block:
            formatted_lines.append('```')
        
        return '\n'.join(formatted_lines)
    
    def _format_html_content(self, content: str) -> str:
        """Format content for HTML export with code block handling"""
        # Handle code blocks marked with ```
        if '```' in content:
            parts = re.split(r'(```.*?```)', content, flags=re.DOTALL)
            formatted_parts = []
            
            for part in parts:
                if part.startswith('```') and part.endswith('```'):
                    # This is a code block
                    code_content = part[3:-3].strip()
                    formatted_parts.append(f'<div class="code-block">{code_content}</div>')
                else:
                    # Regular text - convert newlines to <br>
                    formatted_parts.append(part.replace('\n', '<br>'))
            
            return ''.join(formatted_parts)
        else:
            # No code blocks, just convert newlines
            return content.replace('\n', '<br>')


def export_conversation(agent_id: str, base_dir: Path, config: Any, 
                       messages: List[Dict[str, Any]], format_type: str) -> str:
    """
    Convenience function to export a conversation
    
    Args:
        agent_id: Agent identifier
        base_dir: Base directory for the agent
        config: Agent configuration
        messages: List of conversation messages
        format_type: Export format (json, txt, md, html)
    
    Returns:
        Path to the exported file
    """
    exporter = ConversationExporter(agent_id, base_dir, config, messages)
    return exporter.export_conversation(format_type)


def get_supported_formats() -> Dict[str, Dict[str, str]]:
    """Get information about supported export formats"""
    return EXPORT_FORMATS


def validate_export_format(format_type: str) -> bool:
    """Validate if export format is supported"""
    return format_type.lower() in EXPORT_FORMATS