# komit Roadmap

This roadmap outlines the planned direction of **komit**.

The goal is to evolve komit from a local AI-powered commit message generator into a broader **local AI assistant for Git workflows**, while keeping the experience simple, private, fast, and developer-friendly.

> Status: ✅ Available · 🔄 In progress · 📋 Planned

---

## Current Foundation

komit already provides the core features needed for local AI-assisted commit generation.

| Feature | Status |
|---|---|
| Local commit generation with Ollama | ✅ |
| Conventional, simple, and detailed commit styles | ✅ |
| Branch-aware commit generation | ✅ |
| Commit history context | ✅ |
| Large diff handling | ✅ |
| Deep analysis mode | ✅ |
| Explain staged changes | ✅ |
| Dry-run mode | ✅ |
| Persistent configuration | ✅ |
| Interactive setup | ✅ |
| Shell completion | ✅ |
| Automatic update support | ✅ |
| Linux support | ✅ |
| macOS support | ✅ |
| Windows support | ✅ |
| PyPI distribution | ✅ |
| Binary releases | ✅ |
| Homebrew installation | ✅ |

---

# Upcoming Releases

## v1.1 — Better Project Configuration

> Make komit adapt to each project instead of using the same settings everywhere.

### Repository configuration

Projects will be able to include a `.komit.toml` file containing repository-specific settings.

```text
project/
├── .komit.toml
├── src/
├── tests/
└── ...
```

Example:

```toml
model = "qwen2.5:7b"
style = "conventional"

[commit]
max_subject_length = 72

[scope]
allowed = [
    "api",
    "cli",
    "core",
    "docs"
]
```

Configuration will follow a predictable priority:

```text
Command-line options
        ↓
Repository configuration
        ↓
Global configuration
        ↓
Default values
```

| Feature | Status |
|---|---|
| `.komit.toml` support | 📋 |
| Repository-specific settings | 📋 |
| Configuration priority system | 📋 |
| Configuration validation | 📋 |

---

### Custom commit rules

Repositories will be able to define their own commit conventions.

Example:

```toml
instructions = """
Use Conventional Commits.

Allowed scopes:
- cli
- config
- generator
- git
- docs

Keep commit titles below 72 characters.
"""
```

This will allow komit to follow the conventions already used by a project or team.

| Feature | Status |
|---|---|
| Custom commit instructions | 📋 |
| Custom commit types | 📋 |
| Custom scopes | 📋 |
| Subject length rules | 📋 |
| Repository-specific conventions | 📋 |

---

### Easier configuration management

New CLI commands are planned for inspecting and modifying settings.

```bash
komit config
komit config path
komit config get model
komit config set model qwen3:8b
```

Example:

```text
Current configuration

Model            qwen2.5:7b
Provider         ollama
Style            conventional
Max diff         4000
Timeout          60
Branch context   enabled
```

| Feature | Status |
|---|---|
| `komit config` | 📋 |
| View current configuration | 📋 |
| Modify configuration from the CLI | 📋 |
| Improved configuration errors | 📋 |

---

### Local model management

komit will make it easier to see and select locally installed models.

```bash
komit models
```

Example:

```text
Available models

● qwen2.5:7b
  llama3.2:3b
  mistral:7b

Current model: qwen2.5:7b
```

| Feature | Status |
|---|---|
| List available models | 📋 |
| Show the active model | 📋 |
| Change the active model | 📋 |
| Display model information | 📋 |

---

## v1.2 — More LLM Providers

> Allow users to choose how and where their models run.

Ollama will remain a first-class option, but komit is planned to support additional local and OpenAI-compatible providers.

Potential providers include:

- Ollama
- LM Studio
- llama.cpp servers
- vLLM
- LocalAI
- OpenAI-compatible APIs
- Groq
- Together AI

Example:

```toml
provider = "ollama"
model = "qwen2.5:7b"
```

or:

```toml
provider = "openai-compatible"
base_url = "http://localhost:1234/v1"
model = "qwen3"
```

| Feature | Status |
|---|---|
| Multiple provider support | 📋 |
| Ollama provider | 📋 |
| OpenAI-compatible providers | 📋 |
| LM Studio support | 📋 |
| Custom provider URLs | 📋 |
| Provider validation | 📋 |
| Remote model support | 📋 |

The default experience will continue to favor local models and privacy.

---

## v1.3 — Local AI Git Assistant

> Expand komit beyond commit message generation.

### Code review

A new command is planned for reviewing staged changes before committing.

```bash
komit review
```

Example:

```text
Potential issues

1. generator.py
   HTTP errors may not be handled in this request.

2. config_utils.py
   max_diff input should be validated.

3. tests/
   No test appears to cover the new configuration behavior.
```

The review system may identify:

- Possible bugs
- Missing error handling
- Security concerns
- Missing tests
- Suspicious changes
- Debug code
- Large or unrelated changes
- Configuration issues

| Feature | Status |
|---|---|
| `komit review` | 📋 |
| Per-file review | 📋 |
| Issue severity | 📋 |
| Security warnings | 📋 |
| Test-related warnings | 📋 |
| Review summary | 📋 |

---

### Smart commit splitting

Large commits often contain several unrelated changes.

`komit split` is planned to detect these groups and suggest smaller commits.

```bash
komit split
```

Example:

```text
Suggested commits

1. feat(auth): add token authentication

   src/auth.py
   tests/test_auth.py

2. refactor(db): simplify database connection

   src/database.py

3. ci: update test workflow

   .github/workflows/ci.yml

4. docs: document authentication

   README.md
```

| Feature | Status |
|---|---|
| Detect unrelated changes | 📋 |
| Group related files | 📋 |
| Generate a message for each group | 📋 |
| Preview proposed commits | 📋 |
| Interactive group selection | 📋 |
| Optional automatic commit splitting | 📋 |

---

### Smarter understanding of changes

komit will gradually move from simply reading individual files toward understanding relationships between them.

For example:

```text
src/auth.py
tests/test_auth.py
docs/authentication.md
```

can be recognized as parts of the same feature.

Planned improvements include:

| Feature | Status |
|---|---|
| Semantic file grouping | 📋 |
| Detect code and test relationships | 📋 |
| Detect related documentation | 📋 |
| Better scope detection | 📋 |
| Better commit type detection | 📋 |
| Confidence information | 📋 |

---

## v1.4 — Integrations

> Make komit easier to use from editors, scripts, CI systems, and other tools.

### JSON output

Machine-readable output will allow other applications to integrate with komit.

```bash
komit --json
```

Example:

```json
{
  "message": "feat(cli): add model selection",
  "type": "feat",
  "scope": "cli",
  "description": "add model selection",
  "files": [
    "komit/main.py",
    "komit/config.py"
  ]
}
```

This can enable integrations with:

- Editors
- IDE extensions
- CI/CD pipelines
- Git interfaces
- Shell scripts
- Developer tools

| Feature | Status |
|---|---|
| JSON output | 📋 |
| Structured commit information | 📋 |
| Structured review results | 📋 |
| Structured split results | 📋 |

---

### Git hooks

Optional Git hook integration will make it possible to use komit directly from regular Git workflows.

```bash
komit hook install
```

Potential commands:

```bash
komit hook install
komit hook uninstall
komit hook status
```

| Feature | Status |
|---|---|
| Install Git hooks | 📋 |
| Remove Git hooks | 📋 |
| Check hook status | 📋 |
| `prepare-commit-msg` support | 📋 |

Git hooks will remain optional.

---

### Editor integrations

A VS Code extension is planned as the first editor integration.

Potential features include:

- Generate commit messages
- Explain staged changes
- Review changes
- Regenerate messages
- Select models
- Select commit styles
- View proposed commit groups

| Integration | Status |
|---|---|
| VS Code | 📋 |
| JetBrains IDEs | 📋 |
| Neovim | 📋 |
| Zed | 📋 |

---

## v1.5 — Model Evaluation and Benchmarking

> Provide clearer information about which models work best with komit.

A reproducible benchmark suite is planned to compare different models on real Git changes.

Potentially evaluated models include:

```text
qwen2.5
qwen3
llama
mistral
gemma
```

Metrics may include:

- Commit type accuracy
- Scope accuracy
- Formatting validity
- Commit relevance
- Subject length compliance
- Generation speed
- Hallucination rate

Example:

```text
Model          Type Accuracy   Scope Accuracy   Latency

qwen2.5:7b     92%             84%              2.4s
llama3.2:3b    86%             75%              1.1s
mistral:7b     89%             80%              2.0s
```

| Feature | Status |
|---|---|
| Public benchmark dataset | 📋 |
| Automated benchmark runner | 📋 |
| Model comparison | 📋 |
| Accuracy metrics | 📋 |
| Latency measurements | 📋 |
| Published benchmark results | 📋 |
| Data-based model recommendations | 📋 |

The goal is for model recommendations to eventually be based on measured results instead of subjective labels.

---

# Future Ideas

These features are being considered but are not assigned to a specific release.

## Git workflow

- Interactive staging
- Multiple commit suggestions
- Commit message validation
- Conventional Commit validation
- Oversized commit detection
- Generated file detection
- Lock-file detection
- Automatic scope discovery
- Commit history search

## AI capabilities

- Automatic model selection
- Different models for different tasks
- Confidence scoring
- Explain why a commit type was selected
- Learn repository conventions from Git history
- Repository-aware prompts
- Context-aware code review
- Breaking-change detection

## Repository understanding

komit may optionally use project metadata such as:

```text
README.md
pyproject.toml
package.json
Cargo.toml
go.mod
pom.xml
.gitignore
```

This can provide additional context about the project without sending information outside the configured model provider.

## Distribution

Additional installation methods being considered include:

- Debian/Ubuntu packages
- Fedora packages
- Arch Linux AUR
- Nix packages
- Linux ARM64 binaries
- Windows package managers

---

# Long-Term Direction

komit started as an:

```text
AI-powered commit message generator
```

The long-term direction is to become a:

```text
Local AI assistant for Git workflows
```

while preserving the principles that make the project useful:

- Local-first
- Privacy-focused
- Simple to use
- Fast
- Cross-platform
- No mandatory cloud service
- Compatible with small local models
- Easy to integrate into existing Git workflows

The basic experience should always remain simple:

```bash
git add .
komit
```

Advanced functionality should be available only when needed:

```bash
komit review
komit split
komit --explain
komit --deep
komit --json
```

---

# Documentation

> Make komit easy to learn, configure, troubleshoot, and contribute to.

As the project grows, documentation will be expanded beyond the main README.

## Existing documentation

| Documentation | Status |
|---|---|
| README | ✅ |
| Changelog | ✅ |
| Contributing guide | ✅ |
| Roadmap | ✅ |
| Issue templates | ✅ |

---

## Planned documentation

A dedicated documentation directory is planned:

```text
docs/
├── getting-started.md
├── configuration.md
├── repository-config.md
├── models.md
├── providers.md
├── commands.md
├── architecture.md
├── integrations.md
├── benchmarking.md
└── troubleshooting.md
```

| Guide | Status |
|---|---|
| Getting started | 📋 |
| Configuration | 📋 |
| Repository configuration | 📋 |
| Model selection | 📋 |
| LLM providers | 📋 |
| CLI reference | 📋 |
| Architecture | 📋 |
| Integrations | 📋 |
| Benchmarking | 📋 |
| Troubleshooting | 📋 |

---

## Troubleshooting

Documentation will cover common problems such as:

- Ollama not running
- Missing models
- Generation timeouts
- Invalid configuration
- No staged changes
- Large diff truncation
- Provider connection errors
- Shell completion issues
- Installation problems
- Update problems

Platform-specific guidance will be included where necessary for:

- Linux
- macOS
- Windows

---

## Wiki and Documentation Website

The repository documentation will remain the main source of information initially.

A GitHub Wiki may be introduced if the amount of documentation grows significantly.

A dedicated documentation website may also be considered in the future using tools such as:

```text
MkDocs Material
Docusaurus
Sphinx
```

A future documentation site could contain:

```text
Getting Started
├── Installation
├── First Commit
└── Configuration

Guides
├── Models
├── Providers
├── Review
└── Commit Splitting

Reference
├── CLI
├── Configuration
└── JSON Output

Development
├── Architecture
├── Contributing
└── Benchmarks

Help
├── Troubleshooting
└── FAQ
```

The documentation platform will grow together with the project rather than becoming a requirement for using komit.