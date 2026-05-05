# Changelog

All notable changes to this project will be documented in this file.
Format based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
This project adheres to [Semantic Versioning](https://semver.org/).

---

## [Unreleased]

---
## [0.2.5] - 2026-05-05

### Added
- `komit-update` command — update via pip for pip users
- `komit-update-binary` command — update via curl for binary users  
- `komit-uninstall` command — remove komit, config, and git alias in one command
- Automatic update check on startup via `check_for_updates()`
- `update_utils.py` — dedicated module for update/uninstall logic
- Config file support (`~/.config/komit/config.toml`) via `platformdirs`
- `komit init` — interactive setup wizard to create config file
- `--dry-run` / `-dr` flag — generate message without committing
- `--version` flag — print current version
- `--config` flag — path to custom config file
- `KomitConfig.from_sources()` — merges CLI flags, config file, and defaults
- `config_utils.py` — config file loading and init logic
- Tests reorganized into `tests/cli/` and `tests/unit/`

### Fixed
- Merged `build.yaml` into `release.yaml` — artifacts now transfer correctly
- Fixed Windows binary artifact path (`.exe` suffix handling)
- Added `ollama`, `httpx`, `platformdirs` to PyInstaller dependencies
- Fixed `ci.yaml` folder typo (`.github/workflow` → `.github/workflows`)
- Updated `setup-uv` from `v3` to `v6`
- Tests now isolated from real config file via `isolate_config` fixture

### Changed
- `KomitConfig` now supports merging from CLI args and config file
- Test suite reorganized into `tests/cli/` and `tests/unit/` subdirectories

---

## [0.2.4] - 2026-05-04

### Fixed
- Removed stale `update` import from `main.py` causing ImportError on startup


---
## [0.2.2] - 2026-05-05

### Added
- `ROADMAP.md` — full development roadmap with phases and status
- `CONTRIBUTING.md` — contribution guide with setup, structure, and PR process
- `update_utils.py` — extracted update logic into its own module

### Changed
- Version bumped to `0.2.2`

### Refactored
- Moved update logic from `main.py` to `update_utils.py`
- `main.py` is now cleaner with no update logic mixed in
---

## [0.2.0] - 2026-05-03

### Added
- Version check on startup — notifies when a new version is available
- `komit update` command to update komit from the CLI
- Binary releases for Linux x86_64, macOS Apple Silicon, and Windows x86_64

### Fixed
- Install script now uses GitHub API instead of HTML page for reliable tag extraction
- Install script tag extraction uses portable `grep + sed` instead of `grep -oP` (macOS compatibility)
- Removed stray `)` inside interactive prompt string
- `Commited` typo corrected to `Committed`
- `Stage files` corrected to `Staged files`

---

## [0.1.3] - 2026-05-03

### Added
- CLI flags: `--style` / `-s`, `--model` / `-m`, `--ollama-url` / `-u`, `--max-diff`
- Default style, model, URL and max diff can now be set via flags

---

## [0.1.2] - 2026-05-03

### Fixed
- Install script `exho` typo corrected to `echo`
- Install script "get alias" corrected to "git alias"
- Removed `komit-macos-x86_64` binary (macos-13 runner unavailable on free tier)
- Intel Mac users redirected to `pip install komit` in install script
- `softprops/action-gh-release` updated from `v1` to `v2`
- Added `permissions: contents: write` to publish workflow
- Fixed `uv sync --group dev` to `uv sync --dev` in publish workflow

---

## [0.1.1] - 2026-05-03

### Fixed
- Corrected branch name in install script URL (`main` → `master`)
- Fixed broken `grep` regex for extracting latest release tag
- Fixed `requires-python` from `3.14` (nonexistent) to `3.13`
- Fixed license in `pyproject.toml` from `MIT` to `Apache-2.0`
- Fixed `STYLES.get()` fallback returning string `"conventional"` instead of actual prompt
- Fixed `release.yaml` referencing wrong path `commit_helper/main.py`
- Fixed binary name `kommit` (double-m) to `komit` in release workflow
- Added `check=True` to `commit()` and `commit_with_editor()` so failures raise errors
- Added default `case _:` branch to interactive prompt match statement
- Added error handling for regenerate path in interactive loop

---

## [0.1.0] - 2026-05-03

### Added
- AI-powered commit message generation using Ollama
- Three commit styles: `conventional`, `simple`, `detailed`
- Interactive prompt with `y` / `n` / `e` / `r` options
- Git alias support (`git ai`)
- Cross-platform installation script (`scripts/install.sh`)
- Uninstall script (`scripts/uninstall.sh`)
- Shell script wrapper (`scripts/commit.sh`)
- Published to PyPI

[Unreleased]: https://github.com/glemiu6/komit/compare/v0.2.0...HEAD
[0.2.5]: https://github.com/glemiu6/komit/compare/v0.2.4...v0.2.5
[0.2.2]: https://github.com/glemiu6/komit/compare/v0.2.0...v0.2.2
[0.2.0]: https://github.com/glemiu6/komit/compare/v0.1.3...v0.2.0
[0.1.3]: https://github.com/glemiu6/komit/compare/v0.1.2...v0.1.3
[0.1.2]: https://github.com/glemiu6/komit/compare/v0.1.1...v0.1.2
[0.1.1]: https://github.com/glemiu6/komit/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/glemiu6/komit/releases/tag/v0.1.0