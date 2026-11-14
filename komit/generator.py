"""Generate Git commit messages and explanations using configured LLM providers."""

import httpx

from komit.git_utils import (
    allocate_diff,
    get_changed_files,
    get_recent_commits,
    parse_branch_name,
    split_diff_by_file,
)
from komit.komitconfig import KomitConfig
from komit.message_validation import validate_commit_message
from komit.providers.base import LLMProvider
from komit.providers.factory import create_provider
from komit.providers.ollama import OllamaProvider

STYLES = {
    "conventional": (
        "Generate a Conventional Commit message (type: description).\n"
        "Types: feat, fix, docs, style, refactor, test, chore, perf, ci, build.\n"
        "Format with branch: 'type: description [branch-name]'\n"
        "Example: 'feat: add user authentication [feature/login]'\n"
        "Return only the commit message as plain text."
    ),
    "simple": (
        "Generate a short, clear, single-line commit message in the imperative mood.\n"
        "Format with branch: 'Description [branch-name]'\n"
        "Example: 'Add user authentication [feature/login]'\n"
        "Return only the commit message as plain text."
    ),
    "detailed": (
        "Generate a commit message with a short title and supporting bullet points.\n"
        "Append the branch name in brackets to the title line, if provided.\n"
        "Example:\n"
        "feat: add user authentication [feature/login]\n\n"
        "- Add login endpoint\n"
        "- Add JWT token generation\n"
        "Return only the commit message as plain text."
    ),
}

SYSTEM_PROMPT_TEMPLATE = """\
You are a developer tool that creates accurate Git commit messages from staged diffs.

1. Follow this style exactly:
{style_rules}

2. Branch handling:
{branch_context}

3. Focus:
- Describe what actually changed; do not invent features or fixes.
- Prioritize code changes over documentation when both are present.
- Ignore CHANGELOG.md and ROADMAP.md when deciding the commit type.

4. Output:
- Output only the raw commit message.
- Do not include explanations, Markdown fences, or other commentary.
- Do not add empty brackets or parentheses.
"""

EXPLAIN_SYSTEM_PROMPT = (
    "You are a code reviewer. Explain what the Git diff changes in plain English. "
    "Use a concise numbered list, grouping related changes when appropriate. "
    "Focus on what changed and why it matters. Avoid Markdown formatting."
)

SUMMARIZE_SYSTEM_PROMPT = (
    "You are a senior software developer. Summarize this file's Git diff "
    "in one short English sentence. Focus on what changed. "
    "Return plain text only, without Markdown."
)


def _create_checked_provider(config: KomitConfig) -> LLMProvider:
    """Create the provider and perform checks specific to Ollama."""
    provider = create_provider(config)

    # Only Ollama requires these Ollama-specific availability checks.
    if isinstance(provider, OllamaProvider):
        if not provider.check_ollama_running(config.ollama_url):
            raise RuntimeError("Ollama is not running. Start it with `ollama serve` and try again.")
        if not provider.model_exist(config.ollama_url):
            raise RuntimeError(
                f"Model `{config.model}` is not installed. Run `ollama pull {config.model}`."
            )

    return provider


def _generate_text(
    provider: LLMProvider,
    system_prompt: str,
    user_prompt: str,
    timeout: int,
) -> str:
    """Make one model request and normalize the returned text."""
    try:
        response = provider.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
        )
    except httpx.TimeoutException as exc:
        raise RuntimeError(
            f"Generation timed out after {timeout}s. Try a longer timeout or a smaller model."
        ) from exc

    if not isinstance(response, str):
        raise ValueError("The LLM provider returned a non-text response.")
    return response.strip()


def _branch_context(branch_info: str) -> str:
    """Build branch instructions without inventing a branch name."""
    active_branch = branch_info.strip()
    if not active_branch or active_branch.lower() == "unreleased":
        return (
            "No branch name is available. Do not append brackets, "
            "placeholders, or guessed branch names."
        )

    parsed_branch = parse_branch_name(active_branch)
    context = f"CURRENT GIT BRANCH: {active_branch}\n"
    if parsed_branch["type"]:
        context += f"INFERRED COMMIT TYPE: {parsed_branch['type']}\n"
    if parsed_branch["scope"]:
        context += f"INFERRED SCOPE: {parsed_branch['scope']}\n"
    context += (
        f"Append exactly '[{active_branch}]' to the end of the title line. "
        "Do not append it to any body lines."
    )
    return context


def _summarize_file_with_provider(
    filename: str,
    chunk: str,
    provider: LLMProvider,
    timeout: int,
) -> str:
    summary = _generate_text(
        provider,
        SUMMARIZE_SYSTEM_PROMPT,
        f"File: {filename}\n\n{chunk}",
        timeout,
    )
    if not summary:
        raise ValueError(f"The model returned an empty summary for {filename}.")
    return f"{filename}: {summary}"


def generate_message(
    diff: str,
    config: KomitConfig | None = None,
    branch_info: str = "",
    deep: bool = False,
) -> tuple[str, list[str] | None]:
    """Generate and validate a message for the current staged changes."""
    config = config or KomitConfig()

    changed_files = get_changed_files()
    files_context = f"Modified Files:\n{changed_files}\n\n" if changed_files else ""
    recent = get_recent_commits(3)
    recent_context = f"Recent Commits:\n{recent}\n\n" if recent else ""
    truncated_files: list[str] | None = None

    try:
        # Reuse the same client for deep-mode summaries and the final request.
        provider = _create_checked_provider(config)

        if deep:
            chunks = split_diff_by_file(diff)
            summaries = [
                _summarize_file_with_provider(filename, chunk, provider, config.timeout)
                for filename, chunk in chunks.items()
            ]
            diff = "File summaries:\n" + "\n".join(summaries)
        else:
            diff, truncated_files = allocate_diff(diff, config.max_diff_length)

        style = config.style if config.style in STYLES else "conventional"
        system_prompt = SYSTEM_PROMPT_TEMPLATE.format(
            style_rules=STYLES[style],
            branch_context=_branch_context(branch_info),
        )
        user_prompt = (
            "Review this staged Git diff and generate the commit message:\n\n"
            f"{recent_context}{files_context}Git Diff:\n{diff}"
        )
        message = _generate_text(provider, system_prompt, user_prompt, config.timeout)
        validate_commit_message(message, style)
        return message, truncated_files

    except RuntimeError:
        raise
    except Exception as exc:
        raise RuntimeError(f"Failed to generate commit message: {exc}") from exc


def explain_changes(diff: str, config: KomitConfig | None = None) -> str:
    """Explain the staged diff without generating or making a commit."""
    config = config or KomitConfig()
    if len(diff) > config.max_diff_length:
        diff = diff[: config.max_diff_length] + "\n... (truncated)"

    try:
        provider = _create_checked_provider(config)
        explanation = _generate_text(
            provider,
            EXPLAIN_SYSTEM_PROMPT,
            f"Explain these changes:\n\n{diff}",
            config.timeout,
        )
        if not explanation:
            raise ValueError("The model returned an empty explanation.")
        return explanation
    except RuntimeError:
        raise
    except Exception as exc:
        raise RuntimeError(f"Failed to explain changes: {exc}") from exc


def summarize_file_chunk(
    filename: str,
    chunk: str,
    config: KomitConfig | None = None,
) -> str:
    """Summarize one file diff using the configured provider."""
    config = config or KomitConfig()
    try:
        provider = _create_checked_provider(config)
        return _summarize_file_with_provider(filename, chunk, provider, config.timeout)
    except RuntimeError:
        raise
    except Exception as exc:
        raise RuntimeError(f"Failed to summarize {filename}: {exc}") from exc
