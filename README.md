# 🤖 komit

AI-powered git commit message generator using local LLMs via Ollama. No API keys, no internet required — runs completely locally and privately.

---

[![PyPI](https://img.shields.io/pypi/v/komit)](https://pypi.org/project/komit)
[![Python](https://img.shields.io/pypi/pyversions/komit)](https://pypi.org/project/komit)
[![License](https://img.shields.io/github/license/glemiu6/komit)](https://github.com/glemiu6/komit/blob/master/LICENSE)
[![Downloads](https://static.pepy.tech/badge/komit/month)](https://pepy.tech/project/komit)
[![CI](https://github.com/glemiu6/komit/actions/workflows/ci.yaml/badge.svg)](https://github.com/glemiu6/komit/actions)
[![codecov](https://codecov.io/gh/glemiu6/komit/branch/master/graph/badge.svg)](https://codecov.io/gh/glemiu6/komit)

---

[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-ffdd00?style=flat&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/glemiu6)

---

## Features

- 🧠 **Local LLM** — uses Ollama, no API keys needed
- 🌿 **Branch-Aware Context** — infers conventional types and scopes directly from your active git branch
- 📝 **Multiple commit styles** — conventional, simple, detailed
- 🔍 **Smart diff allocation** — per-file context budget, code files prioritized over docs
- 🔎 **Deep mode** — summarize each file separately for better messages on large changesets
- 💡 **Explain mode** — summarize what changed without committing
- 🕐 **Recent commits context** — last 3 commits included in the prompt for better inference
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
| --- | --- |
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
```

### Subcommands & Maintenance

```bash
komit init       # create or overwrite your config file
komit update     # update to the latest version
komit uninstall  # remove komit from your system
```

### CLI flags

| Flag | Short | Type | Default | Description |
| --- | --- | --- | --- | --- |
| `--style` | `-s` | `conventional`, `simple`, `detailed` | config | Commit message format |
| `--model` | `-m` | String | config | Ollama model to use |
| `--ollama-url` | `-u` | URL | config | Ollama API endpoint |
| `--max_diff` | — | Integer | config | Max diff length in characters |
| `--timeout` | — | Integer | config | LLM request timeout in seconds |
| `--include_branch_name` | `-ib` | Bool | config | Append branch name to commit message |
| `--dry-run` | `-dr` | Flag | `False` | Preview message without committing |
| `--explain` | — | Flag | `False` | Explain staged changes without committing |
| `--deep` | — | Flag | `False` | Summarize each file separately (slower, better on large diffs) |
| `--config` | — | Path | — | Path to a custom config file |

### Examples

```bash
# simple style
komit --style simple

# use a faster model
komit --model llama3.2:3b

# preview without committing
komit --dry-run

# explain what changed without committing
komit --explain

# better messages on large diffs (slower)
komit --deep

# include branch name in the message
komit --include_branch_name True

# remote Ollama instance
komit --ollama-url http://192.168.1.10:11434
```

---

## Interactive Experience

```text
╭──────────────────────── Staged files (3) ────────────────────────╮
│  • src/auth.py                                                    │
│  • tests/test_auth.py                                             │
│  • README.md                                                      │
╰───────────────────────────────────────────────────────────────────╯
Branch name: feat/auth-tokens
Model: qwen2.5:7b · Style: conventional

⠋ Generating commit message...

╭──────────────────── Suggested commit message ─────────────────────╮
│ feat: add JWT authentication token engine [feat/auth-tokens]      │
╰───────────────────────────────────────────────────────────────────╯

» Choose an action: (y)es, (n)o, (e)dit, (r)egenerate (y):
```

| Option | Key | Behavior |
| --- | --- | --- |
| Yes | `y` | Commit with the generated message |
| No | `n` | Cancel without committing |
| Edit | `e` | Open your editor to modify the message |
| Regenerate | `r` | Generate a new message |

---

## Deep Mode

For large changesets with many files, `--deep` summarizes each file individually before generating the final commit message. More accurate, but slower since it makes one LLM call per file.

```bash
komit --deep
```

---

## Explain Mode

Explains your staged changes in plain English without committing — useful for code review prep or PR descriptions.

```bash
komit --explain
```

---

## Branch Name Parsing

When `--include_branch_name` is enabled, komit reads your branch name to infer the commit type and scope automatically.

| Branch | Inferred type | Inferred scope |
| --- | --- | --- |
| `feat/auth-login` | `feat` | `auth` |
| `fix/ui_button` | `fix` | `ui_button` |
| `refactor/api-layer` | `refactor` | `api` |

Supported types: `feat`, `fix`, `chore`, `docs`, `style`, `refactor`, `test`, `ci`, `perf`.

---

## Configuration

Run `komit init` to create your config file at `~/.config/komit/config.toml`:

```toml
model = "qwen2.5:7b"
style = "conventional"
ollama_url = "http://localhost:11434"
max_diff_length = 4000
timeout = 60
include_branch_name = false
```

CLI flags always override config file values.

---

## Commit Style Outputs

### Conventional (default)

```
feat: add user authentication
fix: resolve null pointer in response pipeline
```

### Simple

```
Add user authentication
Fix null pointer in response pipeline
```

### Detailed

```
feat: add user authentication

- Add JWT token generation pipeline
- Implement password hashing with bcrypt
- Add login and logout endpoints
```

---

## Maintenance

```bash
komit update     # update to latest version
komit uninstall  # remove komit completely
```

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feat/my-cool-feature`)
3. Commit your changes (`komit` 😉)
4. Push to the branch (`git push origin feat/my-cool-feature`)
5. Open a Pull Request

---

## License

[Apache License 2.0](https://github.com/glemiu6/komit/blob/master/LICENSE)