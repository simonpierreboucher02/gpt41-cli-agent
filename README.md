# 🤖 OpenAI Gpt-4.1 Unified Agent System
**Author:** Simon-Pierre Boucher

A professional, unified Python interface for interacting with multiple OpenAI models including GPT-4.1, GPT-4.1-mini, and GPT-4.1-nano. This system provides a legendary user experience with advanced features and modern CLI design.

## ✨ Features

### 🎯 **Multi-Model Support**
- **GPT-4.1**: Advanced model with comprehensive capabilities (5min timeout)
- **GPT-4.1 Mini**: Balanced performance and efficiency (3min timeout) 
- **GPT-4.1 Nano**: Lightweight model optimized for speed (2min timeout)

### 🚀 **Advanced Functionality**
- **File Inclusion**: Use `{filename}` syntax to include file contents in conversations
- **Multi-Format Export**: JSON, TXT, Markdown, and beautiful HTML exports
- **Conversation History**: Persistent storage with search and backup capabilities
- **Interactive Configuration**: Easy setup and customization
- **Professional CLI**: Beautiful, colorful interface with intuitive commands

### 📁 **File Support**
Supports 50+ file types including:
- Programming languages (Python, JavaScript, Go, Rust, etc.)
- Configuration files (JSON, YAML, TOML, etc.)
- Documentation (Markdown, RST, LaTeX, etc.)
- Web files (HTML, CSS, GraphQL, etc.)

## 🛠️ Installation

1. **Clone or download the files**:
   ```bash
   # Ensure you have these 5 files:
   # - main.py
   # - agent.py
   # - config.py
   # - utils.py
   # - export.py
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your OpenAI API key** (one of these methods):
   ```bash
   # Option 1: Environment variable
   export OPENAI_API_KEY="your-api-key-here"
   
   # Option 2: The system will prompt you and save it securely
   ```

## 🎯 Quick Start

### Create Your First Agent
```bash
python main.py --create
```

### Start Chatting
```bash
python main.py --agent-id my-agent
```

### List All Agents
```bash
python main.py --list
```

### Show Available Models
```bash
python main.py --models
```

## 💬 Chat Commands

Once in a chat session, use these commands:

| Command | Description |
|---------|-------------|
| `help` | Show all available commands |
| `history [n]` | Show last n messages (default: 5) |
| `search <term>` | Search conversation history |
| `stats` | Show conversation statistics |
| `config` | Show current configuration |
| `export <format>` | Export conversation (json/txt/md/html) |
| `clear` | Clear conversation history |
| `files` | List available files for inclusion |
| `model` | Show current model information |
| `switch <model>` | Switch to different model |
| `quit` | Exit chat |

## 📊 Usage Examples

### Basic Chat Session
```bash
# Create and start chatting with GPT-4.1
python main.py --agent-id my-coding-assistant --model gpt-4.1

# In chat:
You: Hello! Can you help me with Python?
Assistant: Of course! I'd be happy to help you with Python...
```

### File Inclusion
```bash
# In chat, include file contents:
You: Please review my code: {app.py}
Assistant: I'll review your app.py file...
```

### Export Conversations
```bash
# Export as beautiful HTML
python main.py --agent-id my-agent --export html

# Export as JSON with metadata
python main.py --agent-id my-agent --export json
```

### Advanced Configuration
```bash
# Configure agent interactively
python main.py --agent-id my-agent --config

# Quick temperature override
python main.py --agent-id my-agent --temperature 0.7
```

## 🏗️ Architecture

The system is built with a modular architecture:

### Core Files
- **`main.py`**: Enhanced CLI interface with legendary UX
- **`agent.py`**: Unified agent class supporting all models
- **`config.py`**: Model configurations and settings
- **`utils.py`**: Shared utilities and helper functions
- **`export.py`**: Multi-format conversation export

### Data Structure
```
agents/
├── agent-id/
│   ├── config.yaml          # Agent configuration
│   ├── history.json         # Conversation history
│   ├── secrets.json         # API keys (auto-created)
│   ├── backups/             # Rolling history backups
│   ├── logs/                # Daily logs
│   ├── exports/             # Exported conversations
│   └── uploads/             # File uploads
```

## 🎨 Features Deep Dive

### Model-Specific Optimizations
Each model is optimized for its strengths:
- **GPT-4.1**: Uses standard API format, 5-minute timeout
- **GPT-4.1 Mini**: Uses structured content format, 3-minute timeout  
- **GPT-4.1 Nano**: Uses standard format, 2-minute timeout for speed

### Export Formats
- **JSON**: Complete metadata and conversation data
- **TXT**: Clean plain text format
- **Markdown**: GitHub-flavored markdown with syntax highlighting
- **HTML**: Beautiful, responsive design with statistics and styling

### Security Features
- API keys stored securely in individual agent directories
- Automatic .gitignore updates to prevent key exposure
- Input validation and sanitization
- File size limits (2MB) for inclusions

## 🔧 Advanced Usage

### Environment Variables
```bash
OPENAI_API_KEY=your-key-here    # Your OpenAI API key
```

### Configuration Options
- **Temperature**: 0.0-2.0 (creativity level)
- **Max Tokens**: Response length limit
- **System Prompt**: Custom behavior instructions
- **Streaming**: Real-time response streaming
- **History Size**: Maximum conversation length

### Error Handling
- Automatic retries with exponential backoff
- Graceful timeout handling
- Rate limit management
- Detailed logging for troubleshooting

## 🤝 Contributing

This is a production-ready system designed for professional use. The code follows best practices:
- Type hints throughout
- Comprehensive error handling
- Modular, extensible architecture
- Clean separation of concerns

## 📄 License

Professional code for production use. Ensure you comply with OpenAI's terms of service when using their API.

## 🆘 Support

If you encounter issues:
1. Check the logs in `agents/<agent-id>/logs/`
2. Ensure your API key is valid
3. Verify internet connectivity
4. Check file permissions

---

**Built with ❤️ for the AI development community**
