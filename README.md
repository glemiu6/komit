# 🤖 komit

AI-powered git commit message generator using local LLMs via Ollama. No API keys, no internet required — runs completely locally and privately.

---

[![PyPI](https://img.shields.io/pypi/v/komit)](https://pypi.org/project/komit)
[![Python](https://img.shields.io/badge/python-3.13+-blue)](https://www.python.org)
[![License](https://img.shields.io/github/license/glemiu6/komit)](https://github.com/glemiu6/komit/blob/master/LICENSE)
[![Downloads](https://static.pepy.tech/badge/komit)](https://pepy.tech/project/komit)
[![Downloads](https://static.pepy.tech/badge/komit/month)](https://pepy.tech/project/komit)  
📍 [View the roadmap](ROADMAP.md) · [Open an issue](https://github.com/glemiu6/komit/issues) · [Changelog](CHANGELOG.md)

---

## Features

- 🧠 **Local LLM** — uses Ollama, no API keys needed
- 📝 **Multiple commit styles** — conventional, simple, detailed
- 🔄 **Regenerate** — not happy? generate a new message instantly
- ✏️ **Edit before commit** — open your editor to tweak the message
- ⚙️ **CLI flags** — control style, model, and more from the command line
- 🔔 **Auto update check** — notifies you when a new version is available
- 🌍 **Universal** — works via pip, binary, or shell script
- ⚡ **Fast** — runs on your machine, no network calls to external APIs

---

## Requirements

- [Ollama](https://ollama.com) installed and running
- A local model pulled (e.g. `ollama pull qwen2.5:7b`)

---

## Recommended models

| Model | Size | Best for |
|-------|------|----------|
| `qwen2.5:7b` | 4.7GB | Best quality |
| `llama3.2:3b` | 2.0GB | Fastest |
| `mistral:7b` | 4.1GB | Good balance |

```bash
ollama pull qwen2.5:7b
```

---

## Installation

### Linux / macOS — one line

```bash
curl -fsSL https://raw.githubusercontent.com/glemiu6/komit/master/scripts/install.sh | bash
```


### pip

```bash
pip install komit
```

### pipx (recommended for CLI tools)

```bash
pipx install komit
```

### Download binary manually

Download for your platform from [GitHub Releases](https://github.com/glemiu6/komit/releases/latest):

| Platform            | Binary                      |
|---------------------|-----------------------------|
| Linux x86_64        | `komit-linux-x86_64`        |
| macOS Apple Silicon | `komit-macos-arm64`         |
| Windows             | `komit-windows-x86_64.exe`  |

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

---

## Usage

```bash
# Stage your changes
git add .

# Generate a commit message
komit

# Or via git alias
git ai
```

### CLI flags

```bash
komit [--style STYLE] [--model MODEL] [--ollama-url URL] [--max-diff N]
```

| Flag | Options | Default | Description |
|------|---------|---------|-------------|
| `-s, --style` | `conventional`, `simple`, `detailed` | `conventional` | Commit message style |
| `-m, --model` | any Ollama model | `qwen2.5:7b` | Model to use |
| `-u, --ollama-url` | any URL | `http://localhost:11434` | Ollama server URL |
| `--max-diff` | integer | `4000` | Max diff length sent to model |

### Examples

```bash
komit --style simple
komit --model llama3.2:3b
komit --style detailed --model mistral:7b
komit --ollama-url http://192.168.1.10:11434
komit --max-diff 2000
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

## Commit styles

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

## Update

komit automatically checks for updates on startup and notifies you when a new version is available.


```bash
komit update
```



---

## Uninstall

**All platforms — removes binary, config, and git alias**
```
komit uninstall
```

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for setup instructions and guidelines.

1. Fork the repo
2. Create a feature branch (`git checkout -b feature-name`)
3. Make your changes and add tests
4. Commit your changes (`komit` 😉)
5. Push and open a Pull Request

---

## License

[Apache License 2.0](https://github.com/glemiu6/komit/blob/master/LICENSE)