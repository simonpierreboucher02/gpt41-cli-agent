# 🤖 OpenAI GPT-4.1 Unified Agent System  

**👨‍💻 Author: Simon-Pierre Boucher**  

✨ A **professional, unified Python interface** for interacting with multiple **OpenAI models (GPT-4.1, GPT-4.1 Mini, GPT-4.1 Nano)**.  
This system provides a **legendary user experience** with **advanced features** and a **modern CLI design**.  

---

## ✨ Features  

### 🎯 Multi-Model Support  
- 🔹 **GPT-4.1** → Advanced reasoning & comprehensive capabilities (5 min timeout)  
- 🔹 **GPT-4.1 Mini** → Balanced performance & efficiency (3 min timeout)  
- 🔹 **GPT-4.1 Nano** → Lightweight, speed-optimized model (2 min timeout)  

### 🚀 Advanced Functionality  
- 📁 **File Inclusion** via `{filename}` syntax  
- 📤 **Multi-Format Export**: JSON, TXT, Markdown, HTML  
- 💬 **Persistent Conversation History** with search & backup  
- ⚙️ **Interactive Configuration** for easy setup  
- ✨ **Professional CLI** with beautiful colors & intuitive commands  

### 📁 File Support  
Supports **50+ file types**, including:  
- Programming: `.py`, `.js`, `.go`, `.rs`, etc.  
- Config: `.json`, `.yaml`, `.toml`, etc.  
- Docs: `.md`, `.rst`, `.tex`, etc.  
- Web: `.html`, `.css`, `.graphql`, etc.  

---

## 🛠️ Installation  

1. 📥 **Clone or download the repository** (ensure you have these core files):  
   - `main.py`  
   - `agent.py`  
   - `config.py`  
   - `utils.py`  
   - `export.py`  

2. ⚙️ **Install dependencies**:  
   ```bash
   pip install -r requirements.txt
   ```  

3. 🔑 **Set up your OpenAI API key**:  
   ```bash
   # Option 1: Environment variable
   export OPENAI_API_KEY="your-api-key-here"

   # Option 2: System prompt (stored securely)
   ```  

---

## 🎯 Quick Start  

- ▶️ **Create a new agent**:  
  ```bash
  python main.py --create
  ```  

- 💬 **Start chatting**:  
  ```bash
  python main.py --agent-id my-agent
  ```  

- 📋 **List all agents**:  
  ```bash
  python main.py --list
  ```  

- 🔍 **Show available models**:  
  ```bash
  python main.py --models
  ```  

---

## 💬 Chat Commands  

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
| `switch <model>` | Switch to a different model |
| `quit` | Exit chat |  

---

## 📊 Usage Examples  

### Basic Chat Session  
```bash
python main.py --agent-id my-coding-assistant --model gpt-4.1
```  
Chat Example:  
```
You: Hello! Can you help me with Python?  
Assistant: Of course! I'd be happy to help you with Python...  
```  

### File Inclusion  
```
You: Please review my code: {app.py}  
Assistant: I'll review your app.py file...  
```  

### Export Conversations  
```bash
python main.py --agent-id my-agent --export html  
python main.py --agent-id my-agent --export json  
```  

### Configuration  
```bash
python main.py --agent-id my-agent --config  
python main.py --agent-id my-agent --temperature 0.7
```  

---

## 🏗️ Architecture  

### Core Files  
- **`main.py`** → Enhanced CLI interface  
- **`agent.py`** → Unified agent logic  
- **`config.py`** → Model settings  
- **`utils.py`** → Shared utilities  
- **`export.py`** → Export module  

### Data Structure  
```
agents/
├── agent-id/
│   ├── config.yaml      # Agent configuration
│   ├── history.json     # Conversation history
│   ├── secrets.json     # Secure API key storage
│   ├── backups/         # Rolling backups
│   ├── logs/            # Daily logs
│   ├── exports/         # Exported conversations
│   └── uploads/         # File uploads
```  

---

## 🎨 Features Deep Dive  

- ⚡ **Model-Specific Optimizations** (timeouts adapted by model type)  
- 📤 **Export Formats**: JSON, TXT, Markdown, HTML  
- 🔐 **Security Features**: API key protection, `.gitignore` auto-updates, file limits  
- 🛡️ **Error Handling**: retries, timeouts, logging  

---

## 🔧 Advanced Usage  

- 🔑 **Environment Variables**: `OPENAI_API_KEY=your-key`  
- ⚙️ **Configuration Options**: temperature, max tokens, prompts, streaming  
- 🐞 **Error Handling**: retry logic, exponential backoff, logs  

---

## 🤝 Contributing  

Contributions are welcome!  
This project follows **best practices**:  
- ✅ Type hints  
- ✅ Modular architecture  
- ✅ Comprehensive error handling  
- ✅ Extensible design  

---

## 📄 License  

📜 Professional code for production use.  
Ensure compliance with **OpenAI Terms of Service**.  

---

## 🆘 Support  

1. 📂 Check logs in `agents/<agent-id>/logs/`  
2. 🔑 Validate API key  
3. 🌐 Verify internet connection  
4. 🔐 Ensure file permissions  

---

**2025-08-29**  
*Université Laval*  
