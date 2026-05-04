# Contributing to komit

Thank you for considering contributing to komit!
Every contribution helps — bug reports, feature suggestions, documentation fixes, and code are all welcome.

---

## Table of contents

- [Getting started](#getting-started)
- [Development setup](#development-setup)
- [Project structure](#project-structure)
- [Running tests](#running-tests)
- [Making changes](#making-changes)
- [Commit style](#commit-style)
- [Submitting a pull request](#submitting-a-pull-request)
- [Reporting bugs](#reporting-bugs)
- [Suggesting features](#suggesting-features)

---

## Getting started

Before contributing, please:

1. Check the [open issues](https://github.com/glemiu6/komit/issues) to see if someone is already working on it
2. Check the [roadmap](ROADMAP.md) to understand what's planned
3. For large changes, open an issue first to discuss the approach before writing code

---

## Development setup

### Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) — used for dependency management
- [Ollama](https://ollama.com) — required to run komit locally
- Git

### 1. Fork and clone

```bash
git clone https://github.com/YOUR_USERNAME/komit.git
cd komit
```

### 2. Install dependencies

```bash
uv sync --dev
```

### 3. Pull a model for testing

```bash
ollama pull qwen2.5:7b
```

### 4. Verify everything works

```bash
uv run pytest tests/ -v
```

All tests should pass before you start making changes.

---

## Project structure

```
komit/
├── komit/
│   ├── config.py        # KomitConfig dataclass
│   ├── generator.py     # LLM call + prompt logic
│   ├── git_utils.py     # git subprocess wrappers
    ├── update_utils.py  # update function 
│   └── main.py          # CLI entry point + argparse
├── tests/
│   ├── conftest.py      # shared fixtures
│   ├── test_config.py
│   ├── test_generator.py
│   ├── test_git_utils.py
│   └── test_main.py
├── scripts/
│   ├── install.sh       # Linux/macOS install
│   ├── update.sh        # Linux/macOS update
│   └── uninstall.sh     # Linux/macOS uninstall 
├── pyproject.toml
├── CHANGELOG.md
├── ROADMAP.md
├── Makefile
├── CONTRIBUITING.md
└── README.md
```

### Key files to know

| File                    | Purpose                                                            |
|-------------------------|--------------------------------------------------------------------|
| `komit/config.py`       | All configuration lives here — add new options here first          |
| `komit/generator.py`    | Prompt construction and LLM calls — touch this for smarter commits |
| `komit/git_utils.py`    | All `subprocess` / git calls — keep this free of LLM logic         |
| `komit/main.py`         | CLI flags, user interaction loop — keep this thin                  |
| `komit/uodate_utils.py` | The functions for checking if the systems uses the latest version  |

---

## Running tests

```bash
# Run all tests
uv run pytest tests/ -v

# Run a specific file
uv run pytest tests/test_generator.py -v

# Run a specific test
uv run pytest tests/test_main.py::TestRunChoiceY::test_y_calls_commit -v

# Run with coverage
uv run pytest tests/ --cov=komit --cov-report=term-missing
```

### Writing tests

- Every new feature needs tests
- Every bug fix needs a test that would have caught the bug
- Tests live in `tests/` and mirror the module they test
- Use `unittest.mock.patch` to mock `subprocess`, `ollama.Client`, and `builtins.input`
- See existing tests for examples of how mocking is done in this project

---

## Making changes

### Adding a new CLI flag

1. Add the argument in `parse_args()` in `main.py`
2. Add the corresponding field to `KomitConfig` in `config.py`
3. Wire it up in `run()` when constructing `KomitConfig`
4. Add tests in `test_main.py::TestRunCLIArgs`

### Adding a new commit style

1. Add the new style string to the `STYLES` dict in `generator.py`
2. The `--style` flag choices are auto-generated from `STYLES.keys()` — no other change needed
3. Add a test in `test_generator.py` verifying the correct prompt is sent

### Adding a new git utility

1. Add the function to `git_utils.py`
2. Use `subprocess.run(..., check=True)` for commands that should raise on failure
3. Use `capture_output=True, text=True` for commands whose output you need
4. Add tests in `test_git_utils.py` using `@patch("komit.git_utils.subprocess.run")`

---

## Commit style

This project uses **conventional commits** — and yes, you can use komit itself to generate them.

```
feat: add config file support
fix: correct tag extraction regex in install.sh
docs: update README with Windows install instructions
test: add tests for --style CLI flag
chore: update dependencies
refactor: extract interaction loop into separate function
```

Format: `type: short description` (lowercase, no period at end)

| Type | When to use |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `test` | Adding or fixing tests |
| `refactor` | Code change with no behaviour change |
| `chore` | Build, CI, dependency updates |
| `style` | Formatting, whitespace |


---

## Submitting a pull request

1. Create a branch from `master`:
   ```bash
   git checkout -b feat/your-feature-name
   ```

2. Make your changes and write tests

3. Make sure all tests pass:
   ```bash
   uv run pytest tests/ -v
   ```

4. Commit using conventional commits:
   ```bash
   git add .
   komit  # or git commit -m "feat: your change"
   ```

5. Push and open a PR against `master`:
   ```bash
   git push origin feat/your-feature-name
   ```

6. In your PR description, explain:
   - What the change does
   - Why it's needed
   - How you tested it
   - Any related issues (use `Closes #123` to auto-close)

### PR checklist

- [ ] Tests pass (`uv run pytest tests/ -v`)
- [ ] New features have tests
- [ ] `CHANGELOG.md` updated under `[Unreleased]`
- [ ] No unrelated changes mixed in

---

## Reporting bugs

Open an issue at [github.com/glemiu6/komit/issues](https://github.com/glemiu6/komit/issues) and include:

- Your OS and architecture
- Your Python version (`python --version`)
- Your komit version (`komit --version`)
- Your Ollama version (`ollama --version`)
- The exact command you ran
- The full error output

---

## Suggesting features

Open an issue with the `enhancement` label. Check the [roadmap](ROADMAP.md) first — it may already be planned.

Describe:
- What problem it solves
- How you imagine it working
- Any alternatives you considered

---

## Questions?

Open an issue with the `question` label.

---

Thanks for contributing — every improvement makes komit better for everyone.