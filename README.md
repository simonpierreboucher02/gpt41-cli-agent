# 🤖 OpenAI GPT-4.1 Unified Agent System  

**👨‍💻 Author: Simon-Pierre Boucher**  

<div align="center">  

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)  
![OpenAI](https://img.shields.io/badge/OpenAI-API-green?logo=openai&logoColor=white)  
![License](https://img.shields.io/badge/License-MIT-yellow)  
![Version](https://img.shields.io/badge/Version-1.0.0-purple)  

**A professional, unified Python interface for GPT-4.1 models**  
*Featuring GPT-4.1, GPT-4.1 Mini, and GPT-4.1 Nano with advanced CLI and conversation tools*  

[📦 Features](#-features) • [⚙️ Installation](#-installation) • [🚀 Quick Start](#-quick-start) • [💬 Chat Commands](#-chat-commands) • [📊 Usage Examples](#-usage-examples) • [🏗️ Architecture](#-architecture) • [🎨 Deep Dive](#-features-deep-dive) • [🔧 Advanced Usage](#-advanced-usage) • [📝 License](#-license) • [🤝 Contributing](#-contributing)  

</div>  

---

## ✨ Features  

### 🎯 Multi-Model Support  
- 🔹 **GPT-4.1** → Full advanced model (5 min timeout)  
- 🔹 **GPT-4.1 Mini** → Balanced performance (3 min timeout)  
- 🔹 **GPT-4.1 Nano** → Speed-optimized lightweight model (2 min timeout)  

### 🚀 Advanced Functionality  
- 📁 File inclusion with `{filename}` syntax  
- 📤 Multi-format export: JSON, TXT, Markdown, HTML  
- 💬 Persistent history with search & backup  
- ⚙️ Interactive configuration  
- ✨ Modern, colorful CLI  

### 📁 File Support  
- Programming: `.py`, `.js`, `.go`, `.rs`, etc.  
- Config: `.json`, `.yaml`, `.toml`, etc.  
- Docs: `.md`, `.rst`, `.tex`, etc.  
- Web: `.html`, `.css`, `.graphql`, etc.  

---

## ⚙️ Installation  

1. 📥 Clone/download the repo (ensure files: `main.py`, `agent.py`, `config.py`, `utils.py`, `export.py`)  
2. ⚙️ Install dependencies:  
   ```bash
   pip install -r requirements.txt
   ```  
3. 🔑 Set API key:  
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```  

---

## 🚀 Quick Start  

- ▶️ Create agent:  
  ```bash
  python main.py --create
  ```  

- 💬 Start chatting:  
  ```bash
  python main.py --agent-id my-agent
  ```  

- 📋 List agents:  
  ```bash
  python main.py --list
  ```  

- 🔍 Show models:  
  ```bash
  python main.py --models
  ```  

---

## 💬 Chat Commands  

| Command | Description |
|---------|-------------|
| `help` | Show commands |
| `history [n]` | Last n messages |
| `search <term>` | Search history |
| `stats` | Show statistics |
| `config` | Current config |
| `export <format>` | Export chat |
| `clear` | Clear history |
| `files` | List files |
| `model` | Show model info |
| `switch <model>` | Switch model |
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

- **`main.py`** → CLI interface  
- **`agent.py`** → Core agent class  
- **`config.py`** → Model configs  
- **`utils.py`** → Helpers  
- **`export.py`** → Export module  

Data layout:  
```
agents/
└── {agent-id}/
    ├── config.yaml
    ├── history.json
    ├── secrets.json
    ├── backups/
    ├── logs/
    ├── exports/
    └── uploads/
```  

---

## 🎨 Features Deep Dive  

- ⚡ Model-specific optimizations  
- 📤 Export formats: JSON, TXT, MD, HTML  
- 🔐 Security: API key storage, `.gitignore`, input validation  
- 🛡️ Error handling: retries, timeouts, logging  

---

## 🔧 Advanced Usage  

- 🔑 Env vars: `OPENAI_API_KEY=...`  
- ⚙️ Options: temperature, max tokens, system prompt, streaming  
- 🐞 Error handling: retry logic, logging  

---

## 🤝 Contributing  

- ✅ Type hints  
- ✅ Modular design  
- ✅ Error handling  
- ✅ Extensible architecture  

---

## 📝 License  

MIT License — for professional and educational use.  

---

**2025-08-29**  
*Université Laval*  
