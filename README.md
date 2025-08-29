# 🤖 OpenAI GPT-4.1 Unified Agent System  

**👨‍💻 Author: Simon-Pierre Boucher**  

<div align="center">  

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)  
![OpenAI](https://img.shields.io/badge/OpenAI-API-green?logo=openai&logoColor=white)  
![License](https://img.shields.io/badge/License-MIT-yellow)  
![Version](https://img.shields.io/badge/Version-1.0.0-purple)  

**A professional, unified Python CLI agent for OpenAI GPT-4.1 models**  
*Supports GPT-4.1, GPT-4.1 Mini, and GPT-4.1 Nano with advanced conversation management and exports*  

[✨ Features](#-features) • [⚙️ Installation](#-installation) • [🚀 Quick Start](#-quick-start) • [💬 Chat Commands](#-chat-commands) • [📊 Usage Examples](#-usage-examples) • [🏗️ Architecture](#-architecture) • [🔧 Advanced Usage](#-advanced-usage) • [🔒 Security](#-security) • [🐛 Troubleshooting](#-troubleshooting) • [📄 License](#-license) • [🤝 Contributing](#-contributing)  

</div>  

---

## ✨ Features  

- 🔹 **All GPT-4.1 Models**: GPT-4.1, GPT-4.1 Mini, GPT-4.1 Nano  
- 🎨 **Beautiful CLI**: Colorful interface, intuitive commands  
- 📁 **File Inclusion**: `{filename}` syntax  
- 📤 **Multi-format Export**: JSON, TXT, Markdown, HTML  
- 💬 **Persistent History**: Storage with search & backup  
- ⚙️ **Interactive Configuration**  
- 🛡️ **Error Handling & Logging**  

---

## ⚙️ Installation  

Clone the repository:  
```bash
git clone https://github.com/simonpierreboucher02/gpt41-cli-agent.git
cd gpt41-cli-agent
```

Create and activate a virtual environment (recommended):  
```bash
python -m venv venv
source venv/bin/activate
```

Install dependencies:  
```bash
pip install -r requirements.txt
```

Set your OpenAI API key:  
```bash
export OPENAI_API_KEY=your_api_key_here
```  

---

## 🚀 Quick Start  

### Create your first agent  
```bash
python main.py --create
```  

### Start chatting  
```bash
python main.py --agent-id my-agent
```  

### Use a specific model  
```bash
python main.py --agent-id my-agent --model gpt-4.1-mini
```  

### List all agents  
```bash
python main.py --list
```  

### Show available models  
```bash
python main.py --models
```  

### Export a conversation  
```bash
python main.py --agent-id my-agent --export html
```  

---

## 💬 Chat Commands  

| Command | Description |
|---------|-------------|
| `help` | Show all commands |
| `history [n]` | Show last n messages |
| `search <term>` | Search conversation history |
| `stats` | Show statistics |
| `config` | Show current configuration |
| `export <format>` | Export chat (json/txt/md/html) |
| `clear` | Clear history |
| `files` | List files |
| `model` | Show current model |
| `switch <model>` | Switch to another model |
| `quit` | Exit chat |  

---

## 📊 Usage Examples  

- 🧑‍💻 Basic:  
  ```bash
  python main.py --agent-id coding --model gpt-4.1
  ```  

- 📁 File inclusion:  
  ```
  You: Please review {app.py}
  Assistant: Reviewing app.py...
  ```  

- 📤 Export:  
  ```bash
  python main.py --agent-id my-agent --export html
  python main.py --agent-id my-agent --export json
  ```  

- ⚙️ Config:  
  ```bash
  python main.py --agent-id my-agent --config
  python main.py --agent-id my-agent --temperature 0.7
  ```  

---

## 🏗️ Architecture  

```
gpt41-cli-agent/
├── main.py
├── agent.py
├── config.py
├── utils.py
├── export.py
├── requirements.txt
└── agents/
    └── {agent-id}/
        ├── config.yaml
        ├── history.json
        ├── secrets.json
        ├── backups/
        ├── logs/
        └── exports/
```  

---

## 🔧 Advanced Usage  

- 🔑 Environment vars: `OPENAI_API_KEY=...`  
- ⚙️ Options: temperature, max tokens, system prompt, streaming  
- 🐞 Error handling: retries, logs  

---

## 🔒 Security  

- 🔑 Secure key storage  
- 🚫 Sensitive data excluded from logs/exports  
- ✅ Auto `.gitignore` support  

---

## 🐛 Troubleshooting  

- ❌ Import errors → `pip install -r requirements.txt`  
- 🔑 API key errors → `export OPENAI_API_KEY=...`  
- 🔐 Permission errors → check directories  

---

## 📄 License  

MIT License — professional & educational use.  

---

## 🤝 Contributing  

Contributions welcome!  

---

**2025-08-29**  
*Université Laval*  
