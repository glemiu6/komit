# komit/generator.py
import httpx
import requests

from komit.git_utils import (
    allocate_diff,
    get_changed_files,
    get_recent_commits,
    parse_branch_name,
    split_diff_by_file,
)
from komit.komitconfig import KomitConfig

STYLES = {
    "conventional": (
        "Generate a conventional commit message (type: description).\n"
        "Types: feat, fix, docs, style, refactor, test, chore.\n"
        "Format with branch: 'type: description [branch-name]'\n"
        "Example: 'feat: add user authentication [feature/login]'\n"
        "Just the commit message as plain text, no markdown, no backticks, no code blocks."
    ),
    "simple": (
        "Generate a short, clear commit message in imperative mood.\n"
        "Format with branch: 'Description [branch-name]'\n"
        "Example: 'Add user authentication [feature/login]'\n"
        "Just the commit message as plain text, no markdown, no backticks, no code blocks."
    ),
    "detailed": (
        "Generate a commit message with a short title and bullet points.\n"
        "Format with branch: Append the branch name inside brackets to the title line.\n"
        "Example:\n"
        "feat: add user authentication [feature/login]\n\n"
        "- Add login endpoint\n"
        "- Add JWT token generation\n"
        "Just the commit message as plain text, no markdown, no backticks, no code blocks."
    ),
}

SYSTEM_PROMPT_TEMPLATE = """\
You are an expert developer tool that generates Conventional Commit messages based on git diffs.

CRITICAL INSTRUCTIONS:
1. Follow this specific formatting style EXACTLY:
{style_rules}

2. BRANCH HANDLING RULE: 
{branch_context}

3. FOCUS RULE:
- Prioritize code changes (*.py, *.js, *.ts) over documentation changes (*.md, *.txt).
- If both code and docs are changed, the commit type and description must reflect the code changes.
- Ignore CHANGELOG.md and ROADMAP.md entirely when determining the commit type and message.

4. OUTPUT RULES:
- Do NOT include empty brackets "[]" or empty parentheses "()".
- Do NOT append branch names unless explicitly instructed in the BRANCH HANDLING RULE above.
- Output ONLY the raw commit message text.
- NO markdown formatting, NO backticks, NO code blocks, NO explanations.
"""


def model_exist(url: str, model: str) -> bool:
    try:
        r = requests.get(f"{url}/api/tags", timeout=5)
        models = [m["name"] for m in r.json().get("models", [])]
        return model in models
    except Exception:  # noqa: E722
        return False


def check_ollama_running(url: str) -> bool:
    try:
        r = requests.get(f"{url}/api/tags", timeout=5)
        return r.status_code == 200
    except requests.exceptions.RequestException:
        return False


def generate_message(
    diff: str, config: KomitConfig | None = None, branch_info: str = "", deep: bool = False
) -> tuple[str, list[str] | None]:  # noqa: E501
    config = config or KomitConfig()

    changed_files = get_changed_files()
    files_context = f"Modified Files:\n{changed_files}\n\n" if changed_files else ""

    recent = get_recent_commits(3)
    truncated_files = None
    recent_context = f"Recent Commits:\n{recent}\n\n" if recent else ""
    if deep:
        file_chunk = split_diff_by_file(diff)
        summaries = [summarize_file_chunk(f, c, config) for f, c in file_chunk.items()]
        diff = "File summaries:\n" + "\n".join(summaries)
    else:
        diff, truncated_files = allocate_diff(diff, config.max_diff_length)
    style_rules = STYLES.get(config.style, STYLES["conventional"])
    active_branch = branch_info.strip() if branch_info and branch_info.strip() else ""

    if active_branch and active_branch.lower() != "unreleased":
        parsed_branch = parse_branch_name(active_branch)
        branch_context = f"CURRENT GIT BRANCH: {active_branch}\n"
        if parsed_branch["type"]:
            branch_context += f"INFERRED COMMIT TYPE: {parsed_branch['type']}\n"
        if parsed_branch["scope"]:
            branch_context += f"INFERRED CODESPACE SCOPE: {parsed_branch['scope']}\n"
        branch_context += (
            f"MANDATORY SUFFIX: Use exactly '[{active_branch}]' at the end of the title line."  # noqa: E501
        )
    else:
        branch_context = (
            "MANDATORY RULE: No branch information is available. "
            "Do NOT append any square brackets, placeholders, empty braces '[]', or branch names to the message. "  # noqa: E501
            "Do NOT copy bracket patterns from recent commit history. "
            "Do NOT guess or infer a branch name. "
            "The commit message must end with the description text only — no suffixes of any kind."
        )
    system_prompt = SYSTEM_PROMPT_TEMPLATE.format(
        style_rules=style_rules, branch_context=branch_context
    )
    if not check_ollama_running(config.ollama_url):
        raise Exception(
            "Ollama is not running. Please start it using `ollama serve` and try again."
        )
    if not model_exist(config.ollama_url, config.model):
        raise Exception(
            f"Model `{config.model}` not found locally.\nRun: `ollama pull {config.model}`"
        )
    try:
        from ollama import ChatResponse, Client

        client = Client(host=config.ollama_url, timeout=httpx.Timeout(config.timeout))
        response: ChatResponse = client.chat(
            model=config.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": f"Review this git diff and generate the commit message:\n\n{recent_context}{files_context}Git Diff:\n{diff}",  # noqa: E501
                },
            ],
        )
        con = response.message.content or ""
        return con.strip().strip("`").strip(), truncated_files
    except httpx.TimeoutException:
        raise RuntimeError(
            f"Generation timed out after {config.timeout}s.\n"
            "Try increasing the timeout or using a smaller model."
        )

    except Exception as e:
        raise RuntimeError(f"Failed to generate commit message: {e}")


def explain_changes(diff: str, config: KomitConfig | None = None) -> str:
    config = config or KomitConfig()

    if len(diff) > config.max_diff_length:
        diff = diff[: config.max_diff_length] + "\n... (truncated)"

    if not check_ollama_running(config.ollama_url):
        raise Exception("Ollama is not running. Please start by using `ollama serve`.")
    if not model_exist(config.ollama_url, config.model):
        raise Exception(
            f"Model `{config.model}` not found locally.\nRun `ollama pull {config.model}`"
        )  # noqa: E501

    try:
        from ollama import Client

        client = Client(host=config.ollama_url, timeout=httpx.Timeout(config.timeout))
        response = client.chat(
            model=config.model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a code reviewer. Explain what the following git diff does "
                        "in plain English only. Use a numbered list, one item per changed file or feature. "  # noqa: E501
                        "Be concise, focus on what changed and why it matters. "
                        "No markdown formatting, no bold text, no asterisks, no backticks, plain text only."  # noqa: E501
                    ),
                },
                {"role": "user", "content": f"Explain these changes:\n\n{diff}"},
            ],
        )
        con = response.message.content or ""
        return con.strip().strip("`").strip()
    except httpx.TimeoutException:
        raise RuntimeError(f"Timed out after {config.timeout}s.")
    except Exception as e:
        raise RuntimeError(f"Failed to explain changes: {e}")


def summarize_file_chunk(filename: str, chunk: str, config: KomitConfig | None = None) -> str:
    config = config or KomitConfig()
    from ollama import Client

    client = Client(host=config.ollama_url, timeout=httpx.Timeout(config.timeout))
    response = client.chat(
        model=config.model,
        messages=[
            {
                "role": "system",
                "content": "You are a Senior Software developer. Summarize what changed in this file diff in one short sentence in English only. "  # noqa: E501
                "Be concise, focus on what changed and why it matters. "
                "Plain text only, no markdown, no bold, no asterisks, no backticks.",
            },
            {"role": "user", "content": f"File: {filename}\n\n{chunk}"},
        ],
    )
    con = response.message.content or ""
    return f"{filename}: {con.strip()}"
