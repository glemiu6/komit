#komit/generator.py
import requests
import httpx
from komit.git_utils import parse_branch_name,get_changed_files

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

Strict Output Rules:
1. Format: <type>: <description>
2. Do NOT include empty brackets "[]", empty parentheses "()", or trailing whitespace if a scope or branch context is missing.
3. Example of BAD output: "docs: update README []"
4. Example of GOOD output: "docs: update README and CHANGELOG with new features"

CRITICAL INSTRUCTIONS:
1. Follow this specific formatting style:
{style_rules}

2. BRANCH HANDLING RULE: 
{branch_context}

3. Output ONLY the raw commit message text.
4. Absolutely NO markdown formatting, NO backticks (```), NO code blocks, and NO conversational text or explanations.
"""
def model_exist(url:str,model:str)->bool:
    try:
        r = requests.get(f"{url}/api/tags",timeout=5)
        models = [m["name"] for m in r.json().get("models",[])]
        return model in models
    except:
        return False

def check_ollama_running(url:str)->bool:
    try:
        r = requests.get(f"{url}/api/tags",timeout=5)
        return r.status_code == 200
    except requests.exceptions.RequestException:
        return False


def generate_message(diff:str, config:KomitConfig | None=None,branch_info:str=""):
    config = config or KomitConfig()

    changed_files = get_changed_files()
    files_context = f"Modified Files:\n{changed_files}\n\n" if changed_files else ""

    #truncate large diff
    if len(diff)>config.max_diff_length:
        diff = diff[:config.max_diff_length]+"\n... (truncated)"
    style_rules = STYLES.get(config.style, STYLES["conventional"])
    active_branch = branch_info.strip() if branch_info and branch_info.strip() else ""

    if active_branch and active_branch.lower() != "unreleased":
        parsed_branch = parse_branch_name(active_branch)
        branch_context = f"CURRENT GIT BRANCH: {active_branch}\n"
        if parsed_branch["type"]:
            branch_context += f"INFERRED COMMIT TYPE: {parsed_branch['type']}\n"
        if parsed_branch["scope"]:
            branch_context += f"INFERRED CODESPACE SCOPE: {parsed_branch['scope']}\n"
        branch_context += f"MANDATORY SUFFIX: Use exactly '[{active_branch}]' at the end of the title line."
    else:
        branch_context = "MANDATORY RULE: No branch information is available. Do NOT append any square brackets, placeholders, empty braces '[]', or branch names to the message."

    system_prompt = SYSTEM_PROMPT_TEMPLATE.format(style_rules=style_rules, branch_context=branch_context)
    if not check_ollama_running(config.ollama_url):
        raise Exception(
            "Ollama is not running. Please start it using `ollama serve` and try again."
        )
    if not model_exist(config.ollama_url, config.model):
        raise Exception(f"Model `{config.model}` not found locally.\n"
                        f"Run: `ollama pull {config.model}`")
    try:
        from ollama import Client,ChatResponse
        client = Client(host=config.ollama_url, timeout=httpx.Timeout(config.timeout))
        response: ChatResponse = client.chat(model=config.model,
                               messages=[
                                   {
                                       "role":'system',
                                       "content":system_prompt
                                   },
                                   {
                                       "role":'user',
                                       "content":f"Review this git diff and generate the commit message:\n\n{files_context}Git Diff:\n{diff}"
                                   }
                               ])
        return response.message.content.strip().strip('`').strip()
    except httpx.TimeoutException:
        raise RuntimeError(
            f"Generation timed out after {config.timeout}s.\n"
            "Try increasing the timeout or using a smaller model."
        )

    except Exception as e:
        raise RuntimeError(f"Failed to generate commit message: {e}")
