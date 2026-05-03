## 0.2.0

- Added version check on startup - notifies when a new version is available
- Added `komit-update` command to update from the CLI
- Binary distribution via GitHub Releases for Linux and macOS Apple Silicon
- Cross-platform installation script (`scripts/install.sh`)
- Uninstall script (`scripts/uninstall.sh`)

## 0.1.3
- Add CLI Flags: `--style` `-s` , `--model` `-m`, `--ollama-url` `-u`, `--max_diff`


## 0.1.0 — 2026-05-05
- Initial release
- AI-powered commit message generation using Ollama
- Three commit styles: conventional, simple, detailed
- Interactive prompt with y/n/e/r options
- Git alias support (`git ai`)
- Shell script wrapper (`scripts/commit.sh`)
- Published to PyPI