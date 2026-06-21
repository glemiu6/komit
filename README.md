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
- 🌿 **Branch-Aware Context** — Infers conventional types and scopes directly from your active git branch
- 📝 **Multiple commit styles** — conventional, simple, detailed
- 🔄 **Regenerate** — not happy? generate a new message instantly
- ✏️ **Edit before commit** — open your editor to tweak the message safely (`git commit -m ... -e`)
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

Download the binary for your platform from [GitHub Releases](https://www.google.com/search?q=https://github.com/glemiu6/komit/releases/latest):

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

# or via shell script
./scripts/commit.sh
```

### Subcommands & Maintenance

Instead of creating a commit message, you can manage the application lifetime using these distinct actions:

```bash
komit init       # Interactively build or overwrite your global config.toml file
komit update     # Safely checks for and installs down the latest tracking version
komit uninstall  # Complete system removal (clears global aliases, configs, variables, and packaging)

```

### CLI flags

```bash
komit [--style STYLE] [--model MODEL] [--ollama-url URL] [--max_diff N] [--timeout SEC] [--include_branch_name BOOL] [--dry-run]

```

| Flag | Short | Options / Type                       | Default | Description |
| --- |----|--------------------------------------| - | --- |
| `--style` | `-s` | `conventional`, `simple`, `detailed` | `None` (uses config) | Choose the output template formatting engine |
| `--model` | `-m` | String (any Ollama model tag) | `None` (uses config) | Target local model signature |
| `--ollama-url` | `-u` | Valid URL | `None` (uses config) | Set alternative Ollama API endpoint host |
| `--max_diff` | — | Integer | `None` (uses config) | Maximum diff character truncation length |
| `--timeout` | — | Integer | `None` (uses config) | Maximum generation time frame allowance in seconds |
| `--include_branch_name` | `-ib` | `True` / `False` | `None` (uses config) | Enable context mapping and suffixing with current branch name |
| `--dry-run` | `-dr` | Flag (store_true) | `False` | Halts execution gracefully at preview step without creating a commit |
| `--config` | — | Path String | `None` | Read execution parameters from a non-standard configuration layout |
|`--deep`| — | Flag (store_true) | `False` | Summarize each file separately |

### Examples

```bash
# Force simple formatting mode execution
komit --style simple

# Use smaller parameter scale weights to save resources
komit --model llama3.2:3b

# Track structural tags across distinct remote targets
komit --ollama-url [http://192.168.1.10:11434](http://192.168.1.10:11434)

# Match branch contexts strictly to evaluate output properties
komit -ib True --dry-run

# Run against explicit local parameters
komit --config ~/my-config.toml

```

---

## Interactive Experience

When invoked, `komit` structures your staged workspace and interactive paths using rich terminal layouts:

```text
┬──────────────────────── Staged files (3) ────────────────────────┬
│  • src/auth.py                                                   │
│  • tests/test_auth.py                                            │
│  • README.md                                                     │
┴──────────────────────────────────────────────────────────────────┴
Branch name: feature/auth-tokens
Model: qwen2.5:7b · Style: conventional

⠋ Generating commit message...

┬──────────────────── Suggested commit message ────────────────────┬
│ feat(auth): add JWT authentication token engine [feature/auth-t… │
┴──────────────────────────────────────────────────────────────────┴

» Choose an action: (y)es, (n)o, (e)dit, (r)egenerate [y]: 

```

### Response Path Mappings

| Option | Key | Behavior |
| --- | --- | --- |
| **Yes** | `y` | Instantly runs standard non-interactive `git commit -m` mapping directly to the output. |
| **No** | `n` | Terminates routine execution without impacting staged files. |
| **Edit** | `e` | Executes `git commit -m ... -e`, loading the generated message straight into your local environment editor ($EDITOR) for explicit manual overrides. |
| **Regenerate** | `r` | Restrikes the Ollama Chat API endpoint using structural variance to provide a fresh alternative message option. |

---

## Branch Name Parsing (Smart Inference)

When `--include_branch_name` is enabled, `komit` automatically reads your current Git branch name to guess the correct commit type and scope before asking the AI to write the message. 

If your branch follows common naming patterns like `type/scope-description` or `type-scope`, it extracts the details instantly:

*   **`feat/auth-login`** $\rightarrow$ Type: `feat`, Scope: `auth`
*   **`fix/ui_button`** $\rightarrow$ Type: `fix`, Scope: `ui_button`

### Supported Types
The parser actively detects these standard conventional commit types: 
`feat`, `fix`, `chore`, `docs`, `style`, `refactor`, `test`, `ci`, and `perf`.

---

## Configuration Schema

Run `komit init` to automatically provision a configuration folder or overwrite file defaults. The values are securely maintained globally under `~/.config/komit/config.toml` (or your platform configuration equivalent via `platformdirs` standards):

```toml
model = "qwen2.5:7b"
style = "conventional"
ollama_url = "http://localhost:11434"
max_diff_length = 4000
timeout = 60
include_branch_name = true

```

*Note: Runtime arguments passed via your terminal interface explicitly supersede structural rules defined inside your persistent configurations.*

---

## Commit Style Outputs

### Conventional (Default Pattern)

```text
feat(auth): add user authentication [feature/login]
fix(api): resolve null pointer in response pipeline [bugfix/cors]

```

### Simple

```text
Add user authentication [feature/login]
Fix null pointer in response pipeline [bugfix/cors]

```

### Detailed

```text
feat(auth): add user authentication [feature/login]

- Add JWT token generation pipeline
- Implement password security layers using bcrypt primitives
- Append rotation verification routes

```

---

## Maintenance

```bash
# Upgrading tracking states
komit update

# Completely remove all system components
komit uninstall

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

[Apache License 2.0]()

