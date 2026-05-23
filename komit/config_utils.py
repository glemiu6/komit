# komit/config_utils.py

from platformdirs import user_config_dir
import os
import tomllib

APP_NAME = "komit"


def get_default_config_path():
    config_dir = user_config_dir(APP_NAME)
    os.makedirs(config_dir, exist_ok=True)
    return os.path.join(config_dir, 'config.toml')


def init_config():
    paths = get_default_config_path()
    if os.path.exists(paths):
        choice = input(f"Config file already. Overwrite? (y/n): ").lower()
        if choice != "y":
            return

    model = input("Model [qwen2.5:7b]: ") or "qwen2.5:7b"
    style = input("Style [conventional/simple/detailed]: ") or "conventional"
    url = input("URL [http://localhost:11434]: ") or "http://localhost:11434"
    max_diff = input("Max diff length [4000]: ") or 4000
    timeout = input("Timeout [60]: ") or 60

    include_branch = input("Include branch name [True/False]: ").lower() or "true"
    if include_branch in ["true", "t", "y", "yes"]:
        include_branch_name = "true"
    else:
        include_branch_name = "false"

    content = f"""model = "{model}"
style = "{style}"
ollama_url = "{url}"
max_diff_length = {max_diff}
timeout = {timeout}
include_branch_name = {include_branch_name}
"""
    with open(paths, 'w') as f:
        f.write(content.strip())
    print(f"Config file created at {paths}")


def load_config_file(file_path=None):
    config_file = file_path or get_default_config_path()

    if not os.path.exists(config_file):
        return {}
    try:
        with open(config_file, 'rb') as f:
            return tomllib.load(f)
    except Exception as e:
        print(f"Failed to load config file, using default config")
        return {}