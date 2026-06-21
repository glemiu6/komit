# Roadmap

This document outlines the planned development of komit.
Features are grouped by phase, ordered by priority.

> Status legend: ✅ Done · 🔄 In progress · 📋 Planned

---

## Phase 1 — Solid foundation
> Goal: komit feels like a proper CLI tool

| Feature                                                  | Status |
|----------------------------------------------------------|--------|
| Core commit generation via Ollama                        | ✅ |
| Multiple commit styles (conventional, simple, detailed)  | ✅ |
| `--style`, `--model`, `--ollama-url`, `--max-diff` flags | ✅ |
| Published to PyPI                                        | ✅ |
| Binary releases (Linux, macOS, Windows)                  | ✅ |
| CI/CD with GitHub Actions                                | ✅ |
| Config file (`~/.config/komit/config.toml`)              | ✅ |
| `komit init` — interactive setup wizard                  | ✅ |
| `--version` flag                                         | ✅ |
| `--dry-run` flag                                         | ✅ |
| Ollama running check with friendly error                 | ✅ |
| Model existence check with pull suggestion               | ✅ |
| Timeout handling for LLM calls                           | ✅ |
| PowerShell installer (`install.ps1`) | ✅ |
| Automatic PATH setup on Windows | ✅ |
| Windows uninstall support | ✅ |
| Standardized `komit.exe` install | ✅ |



---

## Phase 2 — UX polish
> Goal: people enjoy using komit, not just tolerate it

| Feature | Status |
|---------|--------|
| Colored output using Rich | ✅ |
| Spinner while generating | ✅ |
| Clean output sections (files / generate / result) | ✅ |
| Better `--help` with usage examples | ✅ |
| Improved interactive prompt wording | ✅ |

---

## Phase 3 — Smarter commits
> Goal: noticeably better commit messages than competitors

| Feature | Status |
|---------|--------|
| Branch detection (`git rev-parse`) | ✅ |
| Branch name parsing → infer type + scope | ✅ |
| Structured prompt (branch + files + diff + conventions) | ✅ |
| Commit history context (last 2–3 commits in prompt) | ✅ |
| `--explain` flag (summarize changes without committing) | ✅ |

---

## Phase 4 — Large diff handling
> Goal: high quality messages even on big changesets

| Feature | Status |
|---------|--------|
| Split diff by file instead of character count | ✅ |
| Summarize each file chunk separately | ✅ |
| Merge chunk summaries into final message | ✅ |
| Better truncation messaging | ✅ |

---



## Phase 5 — Engineering quality
> Goal: industry-grade codebase

| Feature | Status |
|---------|--------|
| pytest-cov + coverage badge | ✅ |
| Full type hints + mypy in CI | ✅ |
| Ruff (lint + format) | ✅ |

---

## Phase 6 — Documentation
> Goal: welcoming to contributors

| Feature                                        | Status |
|------------------------------------------------|--------|
| `CHANGELOG.md` (Keep a Changelog format)       | ✅ |
| `CONTRIBUTING.md`                              | ✅ |
| GitHub issue templates (bug + feature request) | 📋 |
| Auto changelog with git-cliff                  | 📋 |
| `Buy me a coffee` sticker                      |📋| 

---

## Phase 7 — Distribution
> Goal: installable everywhere, across platforms and architectures

| Feature | Status |
|---------|-------|
| Homebrew formula (`brew install komit`) | 📋 |
| Shell completion (`komit --<TAB>`) | 📋 |
| `komit update` self-update command | ✅ |
| Dependabot for dependency updates | 📋 |
| Update scripts via curl/irm (Linux, macOS, Windows) | ✅ |
| Linux ARM64 binary support (`komit-linux-arm64`) | 📋 |

---

## Future ideas

These are not scheduled but may be considered based on demand:

- **LM Studio support** — OpenAI-compatible backend for LM Studio users
- **Multiple backends** — support any OpenAI-compatible API (Groq, Together, vLLM)
- **`apt install komit`** — Debian/Ubuntu package via PPA
- **VS Code extension** — generate commit messages from within the editor
- **Commit templates** — per-repo custom commit conventions
- **`komit review`** — AI review of staged changes before committing

---

## Contributing

Have an idea or want to work on something from this roadmap?
Open an issue or a pull request — contributions are welcome.

See [CONTRIBUTING.md](CONTRIBUTING.md) for setup instructions.