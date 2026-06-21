# Changelog

All notable changes to this project will be documented in this file.
Format based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).


---
## [Unreleased]

### Added
- Working on brew formula for macOS support [homebrew-komit](https://github.com/glemiu6/homebrew-komit)

### Fixed
- Branch detection correction in the system prompt


## [0.5.1]

### Added
- TAB autocompletion for `komit --<flag>`

### Fixed
- `get_recent_commits` error corrected

## [0.4.4]

### Added
- Test coverage with pytest-cov
- Codecov integration for coverage reporting in CI
- mypy type checking in CI
- Ruff linting and format checking in CI
- Full type hints across `generator.py`

### Fixed
- `or` chaining bug in `KomitConfig.from_sources` — `False` values now correctly override defaults
- `import pip` replaced with `importlib.util.find_spec` to satisfy ruff F401


## [0.4.3] - 2026-06-05

### Added
- Better truncation message for large diffs

## [0.4.2] - 2026-05-31
### Added
- `--deep` flag for per-file diff summarization (slower but more accurate on large changesets)
- `--explain` flag to summarize staged changes without committing
- Per-file diff allocation with `split_diff_by_file` and `allocate_diff`
- Priority-based diff truncation — code files get more context than docs


### Fixed
- CHANGELOG.md and ROADMAP.md ignored when determining commit type
- Diff truncation now per-file instead of global character count



## [0.4.0] - 2026-05-30

### Added
- `komit --explain` - explain the commits
- Prompt context include the last 3 commits



## [0.3.5] - 2026-05-23
### Fixed

- `komit --help` flag - improved structure
- Improved interactive prompt wording for the LLM

### Added
- `komit -ib ` - branch detection flag 
- Branch detection in the interactive prompt
- Branch name parsing → infer type + scope

## [0.3.2] - 2026-05-13

### Added
- Rich colored output throughout CLI (update, uninstall, commit flow)
- Spinner while generating commit message
- Staged files displayed in a panel
- Suggested commit message displayed in a panel

### Fixed
- UnicodeDecodeError on macOS when diff contains non-UTF-8 bytes


## [0.3.0] - 2026-05-10

### Added
- Windows support: PowerShell installer (`scripts/install.ps1`)
- Automatic PATH setup on Windows via registry
- Standardized `komit.exe` install (binary renamed on installation)
- Windows uninstall support via `komit uninstall`
- Windows binary update support via `komit update`

### Fixed
- Commit messages no longer wrapped in backticks or Markdown code block
- GitHub API rate limit error on `komit update` - added PyPI fallback for version checking

## [0.2.10] - 2026-05-07

### Fixed

- `git_utils.py` uses encoding `utf-8`
- Timeout handling for LLM calls
- `komit uninstall` command resolved issues with paths
- `install.sh` detects the ARCH and installs in the appropriated path
- `-timeout` flag added


## [0.2.9] - 2026-05-06
### Added

- `generator/model_exist` - checks if the model exists locally
- `generator/check_ollama_running` - checks ollama running

### Fixed
- `workflow/release.yaml` - added `requests` dependencies


---
## [0.2.6] - 2026-05-06

### Added
- `komit update` command - update for everytype of installations
- `komit uninstall` command - uninstall komit for everytype of installations
- `scripts/install.sh` - check where to install komit `usr/local/bin`->Linux or `/opt/homebrew/bin`->macOS or for all `~/.local/bin`
- `komit init` command - interactive setup wizard to create config file

### Changed
- `komit-update`/`komit-update-binary`/`komit-uninstall` commands no longer needed

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

[Unreleased]: https://github.com/glemiu6/komit/compare/v0.4.2...HEAD
[0.5.1]: https://github.com/glemiu6/komit/compare/v0.4.4...v0.5.1
[0.4.4]: https://github.com/glemiu6/komit/compare/v0.4.3...v0.4.4
[0.4.3]: https://github.com/glemiu6/komit/compare/v0.4.2...v0.4.3
[0.4.2]: https://github.com/glemiu/komit/compare/v0.4.0...v0.4.2
[0.4.0]: https://github.com/glemiu/komit/compare/v0.3.5...v0.4.0
[0.3.5]: https://github.com/glemiu6/komit/compare/v0.3.2...v0.3.5
[0.3.2]: https://github.com/glemiu6/komit/compare/v0.3.0...v0.3.2
[0.3.0]: https://github.com/glemiu6/komit/compare/v0.2.10...v0.3.0
[0.2.10]: https://github.com/glemiu6/komit/compare/v0.2.9...v0.2.10
[0.2.9]: https://github.com/glemiu6/komit/compare/v0.2.6...v0.2.9
[0.2.6]: https://github.com/glemiu6/komit/compare/v0.2.5...v0.2.6
[0.2.5]: https://github.com/glemiu6/komit/compare/v0.2.4...v0.2.5
[0.2.2]: https://github.com/glemiu6/komit/compare/v0.2.0...v0.2.2
[0.2.0]: https://github.com/glemiu6/komit/compare/v0.1.3...v0.2.0
[0.1.3]: https://github.com/glemiu6/komit/compare/v0.1.2...v0.1.3
[0.1.2]: https://github.com/glemiu6/komit/compare/v0.1.1...v0.1.2
[0.1.1]: https://github.com/glemiu6/komit/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/glemiu6/komit/releases/tag/v0.1.0