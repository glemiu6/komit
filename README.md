# 🤖 komit

AI-powered git commit message generator using local LLMs via Ollama. No API keys, no internet required — runs completely locally and privately.

---

[![PyPI](https://img.shields.io/pypi/v/komit)](https://pypi.org/project/komit)
[![Python](https://img.shields.io/pypi/pyversions/komit)](https://pypi.org/project/komit)
[![License](https://img.shields.io/github/license/glemiu6/komit)](https://github.com/glemiu6/komit/blob/master/LICENSE)
[![Downloads](https://static.pepy.tech/badge/komit/month)](https://pepy.tech/project/komit)
[![CI](https://github.com/glemiu6/komit/actions/workflows/ci.yaml/badge.svg)](https://github.com/glemiu6/komit/actions)

---

## Features

- 🧠 **Local LLM** — uses Ollama, no API keys needed
- 📝 **Multiple commit styles** — conventional, simple, detailed
- 🔄 **Regenerate** — not happy? generate a new message instantly
- ✏️ **Edit before commit** — open your editor to tweak the message
- ⚙️ **CLI flags** — control style, model, and more from the command line
- 📁 **Config file** — persist your preferences with `komit init`
- 🌍 **Universal** — works via pip, binary, or shell script
- 🪟 **Cross-platform** — Linux, macOS, Windows
- ⚡ **Fast** — runs on your machine, no network calls to external APIs
- 🔒 **Ollama validation** — checks if Ollama is running and model exists before generating
- 🔁 **Smart updates** — detects pip vs binary install and updates accordingly


---

## Requirements

- [Ollama](https://ollama.com) installed and running
- A local model pulled (e.g. `ollama pull qwen2.5:7b`)

---

## Recommended Models

| Model | Size | Best for |
|-------|------|----------|
| `qwen2.5:7b` | 4.7GB | Best quality |
| `mistral:7b` | 4.1GB | Good balance |
| `llama3.2:3b` | 2.0GB | Fastest |

```bash
ollama pull qwen2.5:7b
```

---

## Installation

### Option 1 — One line install (Linux/macOS, no Python required)

```bash
curl -fsSL https://raw.githubusercontent.com/glemiu6/komit/master/scripts/install.sh | bash
```

### Option 2 — Windows PowerShell

```powershell
irm https://raw.githubusercontent.com/glemiu6/komit/master/scripts/install.ps1 | iex
```

### Option 3 — pip

```bash
pip install komit
```

### Option 4 — pipx (recommended for CLI tools)

```bash
pipx install komit
```

### Option 5 — Download binary

Download the binary for your platform from [GitHub Releases](https://github.com/glemiu6/komit/releases/latest):

| Platform | Binary |
|----------|--------|
| Linux x86_64 | `komit-linux-x86_64` |
| macOS Apple Silicon | `komit-macos-arm64` |
| Windows | `komit-windows-x86_64.exe` |

> Intel Mac users: use `pip install komit` instead.

```bash
# Linux/macOS
chmod +x komit-*
sudo mv komit-* /usr/local/bin/komit
```

---

## Setup

### Git alias (recommended)

```bash
git config --global alias.ai '!komit'
```

Now you can use `git ai` as a shortcut.

### Shell completion

```bash
# bash
echo 'eval "$(register-python-argcomplete komit)"' >> ~/.bashrc
source ~/.bashrc

# zsh
echo 'eval "$(register-python-argcomplete komit)"' >> ~/.zshrc
source ~/.zshrc
```

---

## Usage

```bash
# stage your changes
git add .

# generate commit message
komit

# or via git alias
git ai

# or via shell script
./scripts/commit.sh
```

### Subcommands

```bash
komit init       # create config file at ~/.config/komit/config.toml
komit update     # update to latest version
komit uninstall  # remove komit
```

### CLI flags

```bash
komit [--style STYLE] [--model MODEL] [--ollama-url URL] [--max-diff N] [--dry-run]
```

| Flag | Options | Default | Description |
|------|---------|---------|-------------|
| `-s, --style` | `conventional`, `simple`, `detailed` | `conventional` | Commit message style |
| `-m, --model` | any Ollama model | `qwen2.5:7b` | Model to use |
| `-u, --ollama-url` | any URL | `http://localhost:11434` | Ollama server URL |
| `--max-diff` | integer | `4000` | Max diff length sent to model |
| `--dry-run` | — | `false` | Preview message without committing |
| `--config` | path | `~/.config/komit/config.toml` | Path to custom config file |

### Examples

```bash
# use simple style
komit --style simple

# use a faster model
komit --model llama3.2:3b

# detailed style with different model
komit --style detailed --model mistral:7b

# connect to remote Ollama
komit --ollama-url http://192.168.1.10:11434

# preview without committing
komit --dry-run

# use custom config file
komit --config ~/my-config.toml
```

### Interactive prompt

```
Staged files (3):
  - src/auth.py
  - tests/test_auth.py
  - README.md

Generating commit message... (style: conventional, model: qwen2.5:7b)

Suggested message:
  feat: add JWT authentication with refresh token support

Use this message? (y/n/e to edit/r to regenerate):
```

| Key | Action |
|-----|--------|
| `y` | Commit with the suggested message |
| `n` | Cancel |
| `e` | Open editor to modify the message |
| `r` | Regenerate a new message |

---

## Config File

Run `komit init` to create a config file at `~/.config/komit/config.toml`:

```toml
model = "qwen2.5:7b"
style = "conventional"
ollama_url = "http://localhost:11434"
max_diff_length = 4000
```

CLI flags always override the config file.

---

## Commit Styles

### Conventional (default)

```
feat: add user authentication
fix: resolve null pointer in login flow
docs: update API reference
```

### Simple

```
Add user authentication
Fix null pointer in login flow
Update API reference
```

### Detailed

```
feat: add user authentication

- Add JWT token generation
- Add password hashing with bcrypt
- Add refresh token support
```

---

## Update & Uninstall

```bash
# update
komit update

# uninstall
komit uninstall
```

`komit` automatically detects whether you installed via pip or binary and uses the correct update method.

---

## Contributing

1. Fork the repo
2. Create a feature branch (`git checkout -b feature-name`)
3. Commit your changes (`komit` 😉)
4. Push to the branch (`git push origin feature-name`)
5. Open a Pull Request

---

## License

[Apache License 2.0](https://github.com/glemiu6/komit/blob/master/LICENSE)