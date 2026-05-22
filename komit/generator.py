#komit/generator.py
import requests
import httpx


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
You are an expert git assistant. Your sole task is to review a code diff and write a clean, production-ready git commit message.

CRITICAL INSTRUCTIONS:
1. Follow this specific formatting style:
{style_rules}

2. MANDATORY RULE: You MUST append the current git branch name wrapped in square brackets (e.g., [branch-name]) to the main message title as shown in the examples.
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

    #truncate large diff
    if len(diff)>config.max_diff_length:
        diff = diff[:config.max_diff_length]+"\n... (truncated)"
    style_rules = STYLES.get(config.style,STYLES["conventional"])
    active_branch = branch_info.strip() if branch_info and branch_info.strip() else ""
    branch_context = f"CURRENT GIT BRANCH: Use exactly '[{active_branch}]' for your brackets suffix."
    system_prompt = SYSTEM_PROMPT_TEMPLATE.format(style_rules=style_rules,branch_context=branch_context)
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
                                       "content":f"Revies this git diff and generate the commit message:\n\n{diff}"
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
