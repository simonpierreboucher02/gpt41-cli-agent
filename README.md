<div align="center">

# 🤖 GPT-4.1 CLI Agent

### A Professional, Unified Python CLI Interface for OpenAI GPT-4.1 Models

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4.1-412991?style=for-the-badge&logo=openai&logoColor=white)](https://openai.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-F7DF1E?style=for-the-badge&logo=opensourceinitiative&logoColor=black)](LICENSE)
[![Version](https://img.shields.io/badge/Version-1.0.0-00C7B7?style=for-the-badge&logo=semver&logoColor=white)](https://github.com/simonpierreboucher02/gpt41-cli-agent/releases)

[![Stars](https://img.shields.io/github/stars/simonpierreboucher02/gpt41-cli-agent?style=for-the-badge&logo=github&color=FFD700)](https://github.com/simonpierreboucher02/gpt41-cli-agent/stargazers)
[![Forks](https://img.shields.io/github/forks/simonpierreboucher02/gpt41-cli-agent?style=for-the-badge&logo=github&color=4CAF50)](https://github.com/simonpierreboucher02/gpt41-cli-agent/network/members)
[![Issues](https://img.shields.io/github/issues/simonpierreboucher02/gpt41-cli-agent?style=for-the-badge&logo=github&color=E74C3C)](https://github.com/simonpierreboucher02/gpt41-cli-agent/issues)
[![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-brightgreen?style=for-the-badge&logo=githubactions&logoColor=white)](https://github.com/simonpierreboucher02/gpt41-cli-agent/pulls)

[![Maintained](https://img.shields.io/badge/Maintained-Yes-2ECC71?style=for-the-badge&logo=checkmarx&logoColor=white)](https://github.com/simonpierreboucher02/gpt41-cli-agent)
[![Code Style](https://img.shields.io/badge/Code_Style-PEP8-blue?style=for-the-badge&logo=python&logoColor=white)](https://peps.python.org/pep-0008/)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20Windows-lightgrey?style=for-the-badge&logo=windows&logoColor=white)](https://github.com/simonpierreboucher02/gpt41-cli-agent)
[![CLI](https://img.shields.io/badge/Interface-CLI-black?style=for-the-badge&logo=gnometerminal&logoColor=white)](https://github.com/simonpierreboucher02/gpt41-cli-agent)

---

**[✨ Features](#-features) • [📊 Metrics](#-project-metrics) • [🧬 Models](#-model-comparison) • [⚙️ Installation](#️-installation) • [🚀 Quick Start](#-quick-start) • [📖 CLI Reference](#-cli-reference) • [💬 Chat Commands](#-chat-commands) • [📐 Architecture](#-architecture) • [🔧 Configuration](#-configuration) • [📤 Export Formats](#-export-formats) • [🔒 Security](#-security) • [🐛 Troubleshooting](#-troubleshooting) • [🤝 Contributing](#-contributing) • [📄 License](#-license)**

</div>

---

## 📊 Project Metrics

<div align="center">

| Metric | Value |
|--------|-------|
| 📁 Total Source Files | 5 Python modules |
| 📏 Lines of Code | ~2,700+ |
| 🤖 Supported Models | 3 (GPT-4.1, Mini, Nano) |
| 📤 Export Formats | 4 (JSON, TXT, MD, HTML) |
| 🐍 Python Requirement | 3.10+ |
| 📦 Core Dependencies | 3 packages |
| 💾 Conversation Storage | JSON (persistent, per agent) |
| 🔍 Search Support | Full-text history search |
| 🌍 Cross-Platform | Linux, macOS, Windows |
| 📝 Config Format | YAML |
| 🔒 Key Storage | Per-agent `secrets.json` |
| 🗂️ Agent Isolation | Full directory sandboxing |

</div>

---

## 🧬 Model Comparison

<div align="center">

| Model | Context Window | Speed | Cost | Best For |
|-------|---------------|-------|------|----------|
| `gpt-4.1` | 1M tokens | ⭐⭐⭐ | 💰💰💰 | Complex reasoning, deep analysis |
| `gpt-4.1-mini` | 1M tokens | ⭐⭐⭐⭐ | 💰💰 | Balanced tasks, daily use |
| `gpt-4.1-nano` | 1M tokens | ⭐⭐⭐⭐⭐ | 💰 | Fast Q&A, lightweight tasks |

</div>

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 🎯 Core Capabilities
- 🤖 **3 GPT-4.1 Models** — Full, Mini, and Nano variants
- 💬 **Persistent Conversations** — History saved in JSON per agent
- 📁 **File Inclusion** — Inject file contents with `{filename}` syntax
- 🔍 **Full-Text Search** — Search across all your conversation history
- 📊 **Chat Statistics** — Tokens used, message count, timestamps
- 🔄 **Live Model Switching** — Switch models mid-conversation

</td>
<td width="50%">

### 🛠️ Export & Management
- 📤 **4 Export Formats** — JSON, TXT, Markdown, HTML
- 🗂️ **Agent Management** — Create, list, inspect, delete agents
- 📋 **Backup System** — Automatic backups of conversation histories
- 📝 **Structured Logging** — Per-agent logs in dedicated directories
- ⚙️ **YAML Config** — Full configuration per agent (temperature, tokens…)
- 🎨 **Colorful CLI** — Rich terminal output with emoji indicators

</td>
</tr>
<tr>
<td width="50%">

### 🔒 Security & Reliability
- 🔑 **Secure Key Storage** — API keys stored in `secrets.json`, gitignored
- 🛡️ **Input Validation** — Agent IDs, model names, file paths validated
- 🔁 **Retry Logic** — Automatic retry on transient API errors
- 🚫 **Secrets Exclusion** — Keys never appear in logs or exports

</td>
<td width="50%">

### ⚙️ Developer Friendly
- 🧩 **Modular Design** — 5 independent, clean Python modules
- 📐 **Type-Annotated** — Full `typing` support throughout codebase
- 🐍 **Pure Python** — No heavy frameworks, just stdlib + 3 packages
- 🧪 **Testable** — Clean separation of concerns for easy testing

</td>
</tr>
</table>

---

## ⚙️ Installation

### Prerequisites

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/downloads/)
[![pip](https://img.shields.io/badge/pip-latest-3775A9?style=flat-square&logo=pypi&logoColor=white)](https://pip.pypa.io/)
[![OpenAI API Key](https://img.shields.io/badge/OpenAI-API_Key_Required-412991?style=flat-square&logo=openai&logoColor=white)](https://platform.openai.com/api-keys)

### Step 1 — Clone the Repository

```bash
git clone https://github.com/simonpierreboucher02/gpt41-cli-agent.git
cd gpt41-cli-agent
```

### Step 2 — Create a Virtual Environment (Recommended)

```bash
# Create the virtual environment
python -m venv venv

# Activate it — Linux/macOS
source venv/bin/activate

# Activate it — Windows
venv\Scripts\activate
```

### Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

<details>
<summary>📦 Dependencies breakdown</summary>

| Package | Version | Purpose |
|---------|---------|---------|
| `requests` | >=2.31.0 | HTTP calls to OpenAI API |
| `PyYAML` | >=6.0 | Reading/writing YAML config files |
| `colorama` | >=0.4.6 | Cross-platform terminal color support |

</details>

### Step 4 — Set Your OpenAI API Key

```bash
# Linux / macOS
export OPENAI_API_KEY="sk-..."

# Windows (PowerShell)
$env:OPENAI_API_KEY="sk-..."

# Or enter it interactively when creating an agent
python main.py --create
```

---

## 🚀 Quick Start

### Create Your First Agent

```bash
python main.py --create
```

The wizard will prompt you for:
- **Agent ID** — a unique name (e.g. `my-assistant`)
- **Model** — GPT-4.1, GPT-4.1 Mini, or GPT-4.1 Nano
- **System Prompt** — optional persona/instructions
- **API Key** — stored securely in `agents/<id>/secrets.json`

### Start a Chat Session

```bash
python main.py --agent-id my-assistant
```

### Use a Specific Model

```bash
python main.py --agent-id my-assistant --model gpt-4.1-mini
```

### List All Your Agents

```bash
python main.py --list
```

### Show Available Models

```bash
python main.py --models
```

### Export a Conversation

```bash
python main.py --agent-id my-assistant --export html
python main.py --agent-id my-assistant --export md
python main.py --agent-id my-assistant --export json
python main.py --agent-id my-assistant --export txt
```

---

## 📖 CLI Reference

```
usage: main.py [OPTIONS]

OpenAI GPT-4.1 Unified CLI Agent

options:
  -h, --help                Show this help message and exit

Agent Management:
  --create                  Create a new agent interactively
  --agent-id ID             Specify the agent to use (required for chat)
  --list                    List all available agents with their info
  --info                    Show detailed info about an agent
  --delete                  Delete an agent and all its data

Model Selection:
  --model MODEL             Model to use: gpt-4.1 | gpt-4.1-mini | gpt-4.1-nano
  --models                  Display all available models with details

Configuration:
  --config                  Show current agent configuration
  --temperature FLOAT       Set sampling temperature (0.0 – 2.0)
  --max-tokens INT          Set maximum tokens per response
  --system-prompt TEXT      Override the system prompt

Export:
  --export FORMAT           Export conversation: json | txt | md | html

Debug:
  --version                 Show version information
  --verbose                 Enable verbose logging output
```

---

## 💬 Chat Commands

Once inside a chat session, you can use the following in-chat commands:

| Command | Alias | Description |
|---------|-------|-------------|
| `help` | `?` | Show all available chat commands |
| `history [n]` | `h [n]` | Display last `n` messages (default: 10) |
| `search <term>` | `s <term>` | Full-text search in conversation history |
| `stats` | — | Show conversation statistics (tokens, messages, duration) |
| `config` | — | Display current agent configuration |
| `export <format>` | — | Export conversation to `json` / `txt` / `md` / `html` |
| `clear` | — | Clear conversation history (with confirmation) |
| `files` | — | List files available for `{filename}` injection |
| `model` | — | Show the currently active model |
| `switch <model>` | — | Switch to a different model without restarting |
| `backup` | — | Manually trigger a history backup |
| `quit` | `exit`, `q` | Exit the chat session gracefully |

### File Injection Syntax

Include the content of any local file directly in your message:

```
You: Please review {app.py} and suggest improvements
You: Explain this config: {agents/my-assistant/config.yaml}
You: What does {utils.py} do?
```

---

## 📐 Architecture

```
gpt41-cli-agent/
│
├── 📄 main.py              # CLI entry point — argument parsing, session management
├── 🤖 agent.py             # UnifiedOpenAIAgent class — chat, history, API calls
├── ⚙️  config.py            # AgentConfig dataclass, ModelRegistry, YAML I/O
├── 🛠️  utils.py             # ColorUtils, APIClient, FileManager, ValidationUtils
├── 📤 export.py             # Multi-format export engine (JSON, TXT, MD, HTML)
├── 📦 requirements.txt      # Pinned dependencies
│
└── agents/                  # Auto-generated agent data directory
    └── {agent-id}/
        ├── config.yaml      # Model, temperature, system prompt, token settings
        ├── history.json     # Full conversation history (timestamped messages)
        ├── secrets.json     # API key (gitignored automatically)
        ├── backups/         # Auto-backup snapshots of history
        ├── logs/            # Per-agent structured logs
        └── exports/         # Generated export files
```

### Module Responsibilities

| Module | Lines | Role |
|--------|-------|------|
| `main.py` | ~641 | CLI argument parsing, session orchestration, interactive setup wizard |
| `agent.py` | ~492 | Core agent class: send messages, stream responses, manage history |
| `export.py` | ~843 | Converts conversation history to JSON, TXT, Markdown, HTML |
| `utils.py` | ~527 | Color output, API client, file injection, key management, validation |
| `config.py` | ~209 | Config dataclass, YAML serialization, model registry |

---

## 🔧 Configuration

Each agent stores its config in `agents/{agent-id}/config.yaml`:

```yaml
agent_id: my-assistant
model: gpt-4.1-mini
temperature: 0.7
max_tokens: 4096
system_prompt: "You are a helpful assistant."
created_at: "2025-08-29T06:23:23"
```

### Configuration Options

| Parameter | Type | Default | Range | Description |
|-----------|------|---------|-------|-------------|
| `model` | `str` | `gpt-4.1` | See models | The OpenAI model to use |
| `temperature` | `float` | `0.7` | `0.0–2.0` | Creativity / randomness of responses |
| `max_tokens` | `int` | `4096` | `1–32768` | Maximum tokens per response |
| `system_prompt` | `str` | `""` | Any string | System-level instructions / persona |

Override at runtime:

```bash
python main.py --agent-id my-assistant --temperature 0.9 --max-tokens 2048
```

---

## 📤 Export Formats

| Format | Extension | Description |
|--------|-----------|-------------|
| `json` | `.json` | Raw structured conversation with full metadata |
| `txt` | `.txt` | Plain text, human-readable transcript |
| `md` | `.md` | Markdown formatted, ready for docs or GitHub |
| `html` | `.html` | Styled HTML with syntax highlighting, shareable |

Exports are saved to `agents/{agent-id}/exports/` with timestamped filenames.

---

## 📊 Usage Examples

### Code Review Workflow

```bash
# Start a coding assistant agent
python main.py --agent-id code-reviewer --model gpt-4.1

# Inside chat, inject your file
You: Review {main.py} for bugs and code quality issues

# Export the review as Markdown
export md
```

### Document Analysis

```bash
# Use the powerful base model for deep analysis
python main.py --agent-id analyst --model gpt-4.1 --temperature 0.3

# Inject your document
You: Summarize and extract key points from {report.txt}
```

### Fast Q&A Bot

```bash
# Use Nano for fast, cost-effective responses
python main.py --agent-id quickbot --model gpt-4.1-nano

# Rapid fire questions
You: What is the capital of France?
You: Convert 42 Celsius to Fahrenheit
You: List 5 Python list comprehension examples
```

### Full Workflow with Config Override

```bash
python main.py \
  --agent-id my-agent \
  --model gpt-4.1-mini \
  --temperature 0.5 \
  --max-tokens 2048 \
  --system-prompt "You are a senior software architect."
```

---

## 🔒 Security

[![Security](https://img.shields.io/badge/Security-Best_Practices-2ECC71?style=for-the-badge&logo=shield&logoColor=white)](https://github.com/simonpierreboucher02/gpt41-cli-agent)

- 🔑 **API Key Isolation** — Keys are stored in `secrets.json` per agent, never in code or config
- 🚫 **Auto-gitignore** — `secrets.json` and `*.log` files are excluded automatically
- 🧹 **No Logging of Secrets** — API keys are masked in all log output
- ✅ **Input Validation** — All CLI inputs are validated before use
- 📁 **Sandboxed Agents** — Each agent has its own isolated directory tree
- 🔐 **File Permissions** — Sensitive directories created with restricted permissions

> **Best practice:** Never commit your `agents/` directory to version control. Add it to your `.gitignore`.

---

## 🐛 Troubleshooting

<details>
<summary><strong>❌ ModuleNotFoundError or ImportError</strong></summary>

```bash
# Make sure your virtual environment is active
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

</details>

<details>
<summary><strong>🔑 AuthenticationError / Invalid API Key</strong></summary>

```bash
# Check the key is exported
echo $OPENAI_API_KEY

# Re-export it
export OPENAI_API_KEY="sk-..."

# Or recreate the agent and enter the key interactively
python main.py --create
```

</details>

<details>
<summary><strong>🚫 Permission Denied on agents/ directory</strong></summary>

```bash
# Fix permissions on the agents directory
chmod -R 755 agents/
```

</details>

<details>
<summary><strong>💥 Rate Limit Errors (429)</strong></summary>

The agent has built-in retry logic with exponential backoff. If you're still hitting limits:
- Lower `max_tokens` with `--max-tokens 1024`
- Switch to `gpt-4.1-nano` for lighter usage
- Check your [OpenAI usage limits](https://platform.openai.com/usage)

</details>

<details>
<summary><strong>📁 File Injection Not Working</strong></summary>

Make sure the file exists relative to where you run `main.py`:

```bash
# Run from the repo root
python main.py --agent-id my-agent

# Then reference files relative to that location
You: Review {src/app.py}
```

</details>

---

## 🤝 Contributing

Contributions are welcome and appreciated! Here's how to get started:

```bash
# 1. Fork the repo on GitHub

# 2. Clone your fork
git clone https://github.com/YOUR_USERNAME/gpt41-cli-agent.git

# 3. Create a feature branch
git checkout -b feature/my-awesome-feature

# 4. Make your changes, then commit
git add .
git commit -m "feat: add my awesome feature"

# 5. Push and open a Pull Request
git push origin feature/my-awesome-feature
```

### Contribution Guidelines

- Follow [PEP 8](https://peps.python.org/pep-0008/) code style
- Add type annotations to new functions
- Keep modules focused — don't cross module boundaries unnecessarily
- Test your changes before submitting a PR

---

## 👥 Authors

<table>
<tr>
<td align="center" width="50%">

### Simon-Pierre Boucher
**Lead Developer & Architect**

[![GitHub](https://img.shields.io/badge/GitHub-simonpierreboucher02-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/simonpierreboucher02)
[![Email](https://img.shields.io/badge/Email-spbou4%40protonmail.com-8B89CC?style=for-the-badge&logo=protonmail&logoColor=white)](mailto:spbou4@protonmail.com)
[![Website](https://img.shields.io/badge/Website-www.spboucher.ai-00C7B7?style=for-the-badge&logo=safari&logoColor=white)](https://www.spboucher.ai)

*AI/ML researcher and developer. Building intelligent CLI tools and AI pipelines.*

</td>
<td align="center" width="50%">

### Claude (Anthropic)
**README Co-Author & AI Assistant**

[![Anthropic](https://img.shields.io/badge/Anthropic-Claude_Sonnet_4.6-D97757?style=for-the-badge&logo=anthropic&logoColor=white)](https://www.anthropic.com)
[![Claude Code](https://img.shields.io/badge/Claude_Code-CLI-412991?style=for-the-badge&logo=terminal&logoColor=white)](https://claude.ai/claude-code)

*This README was co-authored and structured with the assistance of Claude (Anthropic's AI), used via Claude Code CLI.*

</td>
</tr>
</table>

---

## 📄 License

```
MIT License

Copyright (c) 2025 Simon-Pierre Boucher

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
```

---

<div align="center">

Made with ❤️ by **[Simon-Pierre Boucher](https://www.spboucher.ai)** • [spbou4@protonmail.com](mailto:spbou4@protonmail.com)

[![GitHub](https://img.shields.io/badge/Follow_on_GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/simonpierreboucher02)
[![Website](https://img.shields.io/badge/Visit_Website-00C7B7?style=for-the-badge&logo=safari&logoColor=white)](https://www.spboucher.ai)

*Co-authored with [Claude](https://www.anthropic.com) (Anthropic) via [Claude Code](https://claude.ai/claude-code)*

⭐ **If this project helped you, give it a star!** ⭐

</div>
