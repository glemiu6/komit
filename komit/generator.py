#komit/generator.py
from komit.komitconfig import KomitConfig
STYLES ={
    "conventional":("Generate a conventional commit message (type: description).\n"
                    "Types: feat, fix, docs, style, refactor, test, chore.\n"
                    "Example: 'feat: add user authentication'\n"
                    "Just the message, nothing else"),
    "simple":("Generate a short, clear commit message in imperative mood.\n"
              "Example: 'Add user authentication'\n"
              "Just the message, nothing else"),
    "detailed":("Generate a commit message with a short title and bullet points.\n"
                "Example:\n"
                "feat: add user authentication\n\n"
                "- Add login endpoint\n"
                "- Add JWT token generation\n"
                "- Add password hashing\n"
                "Just the message, nothing else"),
}

def generate_message(diff:str, config: KomitConfig | None=None):
    config = config or KomitConfig()

    #truncate large diff
    if len(diff)>config.max_diff_length:
        diff = diff[:config.max_diff_length]+"\n... (truncated)"
    style_prompt = STYLES.get(config.style,STYLES["conventional"])
    try:
        from ollama import Client
        client = Client(host=config.ollama_url)
        response = client.chat(model=config.model,
                               messages=[
                                   {
                                       "role":'system',
                                       "content":style_prompt
                                   },
                                   {
                                       "role":'user',
                                       "content":f"Generate a commit message for this:\n\n{diff}"
                                   }
                               ])
        return response.message.content.strip()
    except Exception as e:
        raise RuntimeError(f"Failed to generate commit message: {e}")
