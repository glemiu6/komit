# komit/config_utils.py

import os
import tomllib

from platformdirs import user_config_dir

APP_NAME = "komit"


def get_default_config_path() -> str:
    config_dir = user_config_dir(APP_NAME)
    os.makedirs(config_dir, exist_ok=True)
    return os.path.join(config_dir, "config.toml")



def init_config() -> None:
    path = get_default_config_path()

    if os.path.exists(path):
        choice = input("Config already exists. Overwrite? (y/n): ").strip().lower()
        if choice != "y":
            return

    provider = (
        input("Provider [ollama/openai_compatible]: ").strip().lower()
        or "ollama"
    )

    if provider not in ("ollama", "openai_compatible"):
        print(f"Unsupported provider: {provider}")
        return

    model = input("Model [qwen2.5:7b]: ").strip() or "qwen2.5:7b"
    style = input("Style [conventional/simple/detailed]: ").strip() or "conventional"

    if style not in ("conventional", "simple", "detailed"):
        print(f"Unsupported style: {style}")
        return

    try:
        max_diff = int(input("Max diff length [4000]: ") or "4000")
        timeout = int(input("Timeout [60]: ") or "60")
        if max_diff <= 0 or timeout <= 0:
            raise ValueError
    except ValueError:
        print("Max diff length and timeout must be positive integers.")
        return

    include_branch = (
        input("Include branch name [true/false]: ").strip().lower()
        or "true"
    )

    if include_branch not in ("true", "false"):
        print("Include branch name must be true or false.")
        return

    if provider == "ollama":
        url = (
            input("Ollama URL [http://localhost:11434]: ").strip()
            or "http://localhost:11434"
        )
        provider_config = f'ollama_url = "{url}"'
    else:
        url = (
            input("Base URL [http://localhost:8080]: ").strip()
            or "http://localhost:8080"
        )
        provider_config = f'base_url = "{url}"'

    content = f"""model = "{model}"
style = "{style}"
provider = "{provider}"
{provider_config}
max_diff_length = {max_diff}
timeout = {timeout}
include_branch_name = {include_branch}
"""

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Config file created at {path}")



def load_config_file(file_path=None) -> dict:
    config_file = file_path or get_default_config_path()

    if not os.path.exists(config_file):
        return {}
    try:
        with open(config_file, "rb") as f:
            return tomllib.load(f)
    except tomllib.TOMLDecodeError as exc:
        raise ValueError(
                f"Invalid TOML configuration in {config_file}: {exc}") from exc
