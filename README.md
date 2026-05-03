# 🤖 komit

AI-powered git commit message generator using local LLMs via Ollama. No API keys, no internet required — runs completely locally and privately.

---

![PyPI](https://img.shields.io/pypi/v/komit)
![Python](https://img.shields.io/badge/python-3.13+-blue)
![License](https://img.shields.io/github/license/glemiu6/komit)
![Downloads](https://img.shields.io/pypi/dm/komit)

---

## Features

- 🧠 **Local LLM** — uses Ollama, no API keys needed
- 📝 **Multiple commit styles** — conventional, simple, detailed
- 🔄 **Regenerate** — not happy? generate a new message instantly
- ✏️ **Edit before commit** — open your editor to tweak the message
- 🌍 **Universal** — works via pip, binary, or shell script
- ⚡ **Fast** — runs on your machine, no network calls to external APIs

---

## Requirements

- [Ollama](https://ollama.com) installed and running
- A local model pulled (e.g. `ollama pull qwen2.5:7b`)

---

## Installation

### Option 1 — One line install (no Python required)

```bash
curl -fsSL https://raw.githubusercontent.com/glemiu6/komit/main/scripts/install.sh | bash
```

### Option 2 — pip

```bash
pip install komit
```

### Option 3 — Download binary

Download the binary for your platform from [GitHub Releases](https://github.com/glemiu6/komit/releases/latest):

| Platform | Binary |
|----------|--------|
| Linux x86_64 | `komit-linux-x86_64` |
| macOS Apple Silicon | `komit-macos-arm64` |
| macOS Intel | `komit-macos-x86_64` |
| Windows | `komit-windows-x86_64.exe` |

```bash
# Linux/Mac
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
# stage your changes
git add .

# generate commit message
komit

# or via git alias
git ai

# or via shell script
./scripts/commit.sh
```

### Interactive prompt

```
Staged files (3):
  - src/auth.py
  - tests/test_auth.py
  - README.md

Generating commit message...

Suggested message:
  feat: add JWT authentication with refresh token support

Use this message? (y/n/e to edit/r to regenerate): 
```

- `y` — commit with the suggested message
- `n` — cancel
- `e` — open editor to modify the message
- `r` — regenerate a new message

---

## Commit Styles

Configure in `config.py` or pass as argument:

**Conventional** (default):
```
feat: add user authentication
fix: resolve null pointer in login flow
docs: update API reference
```

**Simple:**
```
Add user authentication
Fix null pointer in login flow
Update API reference
```

**Detailed:**
```
feat: add user authentication

- Add JWT token generation
- Add password hashing with bcrypt
- Add refresh token support
```

---

## Configuration

Edit `komit/config.py`:

```python
@dataclass
class KomitConfig:
    model: str = "qwen2.5:7b"       # any Ollama model
    style: str = "conventional"      # conventional, simple, detailed
    max_diff_length: int = 4000      # truncate large diffs
    ollama_url: str = "http://localhost:11434"
```

---

## Recommended Models

| Model | Size | Best for |
|-------|------|----------|
| `qwen2.5:7b` | 4.7GB | Best quality |
| `llama3.2:3b` | 2.0GB | Fastest |
| `mistral:7b` | 4.1GB | Good balance |

```bash
ollama pull qwen2.5:7b
```

---

## Uninstall

```bash
./scripts/uninstall.sh
# or
pip uninstall komit
```

---

## Contributing

1. Fork the repo
2. Create a feature branch (`git checkout -b feature-name`)
3. Commit your changes (`komit` 😉)
4. Push to the branch (`git push origin feature-name`)
5. Open a Pull Request

---

## License

[Apache License](LICENSE)