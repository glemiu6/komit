# 🤖 komit

AI-assisted Git commit messages from your staged changes. Komit reads the diff, recent commit history, changed files, and—optionally—the current branch, then suggests a commit message you can review before committing.

It runs locally by default with Ollama and also supports OpenAI-compatible providers.

[![PyPI](https://img.shields.io/pypi/v/komit)](https://pypi.org/project/komit)
[![Python](https://img.shields.io/pypi/pyversions/komit)](https://pypi.org/project/komit)
[![License](https://img.shields.io/github/license/glemiu6/komit)](https://github.com/glemiu6/komit/blob/master/LICENSE)
[![Downloads](https://static.pepy.tech/badge/komit/month)](https://pepy.tech/project/komit)

## Highlights

- **Provider-based LLM integration** — use Ollama or an OpenAI-compatible API through one configuration surface.
- **Context-aware messages** — uses staged diffs, modified files, recent commits, and branch-derived type/scope hints.
- **Three output styles** — Conventional Commits, simple one-line messages, or detailed messages with bullet points.
- **Large-diff support** — allocates context per file and offers `--deep` mode for file-by-file summaries.
- **Safe review workflow** — preview with `--dry-run`, explain changes with `--explain`, regenerate, edit, or cancel before committing.
- **Validated output** — rejects malformed model responses and checks Ollama availability and local model installation before generation.
- **Portable CLI** — install with pip, pipx, Homebrew, a binary, PowerShell, or Nix; supports Linux, macOS, and Windows.

## Quick start

Install Komit and pull a local model:

```bash
pipx install komit
ollama pull qwen2.5:7b
```

Stage changes and run Komit:

```bash
git add .
komit
```

Komit shows the staged files and proposed message, then lets you accept, reject, edit, or regenerate it. Use it as a Git alias if preferred:

```bash
git config --global alias.ai '!komit'
git ai
```

## Providers

Ollama is the default and requires a running Ollama server with the selected model installed:

```bash
komit --provider ollama --model qwen2.5:7b
```

For an OpenAI-compatible server, select the provider and set its base URL:

```bash
komit \
  --provider openai_compatible \
  --base-url http://localhost:8080/v1 \
  --model your-model
```

## Useful commands

```bash
komit --dry-run       # generate without committing
komit --explain       # explain staged changes without committing
komit --deep          # summarize files before generating the message
komit --style simple  # choose conventional, simple, or detailed output
komit --model mistral:7b
komit init            # create the user configuration file
komit update          # update Komit
komit uninstall       # remove Komit
```

## Configuration

Run `komit init` to create `~/.config/komit/config.toml` (platform-dependent config directory). CLI options override values from the file.

```toml
model = "qwen2.5:7b"
style = "conventional"
provider = "ollama"
ollama_url = "http://localhost:11434"
base_url = "http://localhost:8080/v1"
max_diff_length = 4000
timeout = 60
include_branch_name = true
```

The main configuration options are `provider`, `model`, `style`, `ollama_url`, `base_url`, `max_diff_length`, `timeout`, and `include_branch_name`.

## Download and installation options

### Prebuilt binaries

Download the latest release from [GitHub Releases](https://github.com/glemiu6/komit/releases/latest):

| Platform | Download |
| --- | --- |
| Linux x86_64 | `komit-linux-x86_64` |
| macOS Apple Silicon | `komit-macos-arm64` |
| Windows x86_64 | `komit-windows-x86_64.exe` |
| macOS Intel | Use `pip`, Homebrew, or the installer below; no Intel binary is currently published. |

On Linux and macOS, make the downloaded binary executable and place it on your `PATH`:

```bash
chmod +x komit-*
sudo mv komit-* /usr/local/bin/komit
```

### Installers and package managers

```bash
# pip / pipx
pip install komit
pipx install komit

# Homebrew
brew tap glemiu6/komit && brew install komit

# Linux/macOS installer
curl -fsSL https://raw.githubusercontent.com/glemiu6/komit/master/scripts/install.sh | bash

# Nix
nix profile install github:glemiu6/komit
nix run github:glemiu6/komit
```

Windows users can run the PowerShell installer:

```powershell
irm https://raw.githubusercontent.com/glemiu6/komit/master/scripts/install.ps1 | iex
```

Nix supports Linux and macOS, including Intel and Apple Silicon systems. Nix-managed installations should be updated or removed with Nix rather than `komit update` or `komit uninstall`.

## Requirements

- Python 3.13+ for Python installations
- A configured LLM provider
- For Ollama: [Ollama](https://ollama.com) running locally or at the configured URL, with a model pulled

## License

[Apache License 2.0](https://github.com/glemiu6/komit/blob/master/LICENSE)
