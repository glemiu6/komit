#!/usr/bin/env python3
#komit/main.py
import subprocess
import sys
import argparse
from komit.git_utils import get_staged_files,get_staged_diff,is_git_repo,commit,commit_with_editor
from komit.generator import generate_message,STYLES
from komit.komitconfig import KomitConfig
def check_for_updates():
    try:
        import httpx
        from komit import __version__
        response= httpx.get(
            "https://api.github.com/repos/glemiu6/komit/releases/latest",
            timeout=2
        )
        latest= response.json()["tag_name"].lstrip("v")
        if latest != __version__:
            print(f"!!  New version available: v{latest} (you have v{__version__})")
            print(f"    Run: komit-update\n")
    except Exception:
        pass
def update()->None:
    print("Updating komit...")
    result = subprocess.run(["curl","-fsSL","https://raw.githubusercontent.com/glemiu6/komit/master/scripts/install.sh"],capture_output=True,text=True)
    subprocess.run(['bash'],input=result.stdout)
    print("Done!")
def parse_args():
    parser = argparse.ArgumentParser(
        prog="komit",
        description="AI-powered git commit message generator using local LLMs via Ollama."
    )
    parser.add_argument(
        '-s',
        '--style',
        choices=list(STYLES.keys()),
        default='conventional',
        help="Choose the style of the commit message (default: conventional)."
    )
    parser.add_argument(
        '-m',
        '--model',
        default='qwen2.5:7b',
        help="Choose the model (default: qwen2.5:7b)."
    )
    parser.add_argument(
        '--ollama-url',
        '-u',
        default='http://localhost:11434',
        help="Choose the URL of the Ollama (default: http://localhost:11434)."
    )
    parser.add_argument(
        '--max_diff',
        default=4000,
        type=int,
        help="Choose the maximum diff length (default: 4000)."
    )
    return parser.parse_args()
def run():
    check_for_updates()
    args = parse_args()
    if not is_git_repo():
        print("Not a git repository")
        sys.exit(1)
    diff = get_staged_diff()
    if not diff:
        print("No staged changes. Run 'git add' first.")
        sys.exit(1)
    files= get_staged_files()
    print(f"\nStaged files ({len(files)}):")
    for f in files:
        print(f"  - {f}")
    print("\nGenerating commit message...")
    config = KomitConfig(model=args.model,
                         style=args.style,
                         max_diff_length=args.max_diff,
                         ollama_url=args.ollama_url
                         )
    print(f"\nGenerating commit message... (style: {config.style}, model: {config.model})")
    try:

        message= generate_message(diff=diff,config=config)
    except RuntimeError as e:
        print(f"Error: {e}")
        sys.exit(1)
    print(f"\nSuggested message:\n {message}")
    while True:
        choice= input("\nUse this message? (y/n/e to edit/r to regenerate): ").strip().lower()
        match choice :
            case 'y':
                try:
                    commit(message)
                    print("Committed!")
                except subprocess.CalledProcessError as e:
                    print(f"Commit failed: {e}")
                    sys.exit(1)
                break
            case 'n':
                print("Commit cancelled!")
                break
            case 'e':
                try:
                    commit_with_editor(message)
                except subprocess.CalledProcessError as e:
                    print(f"Commit failed: {e}")
                    sys.exit(1)
                break
            case 'r':
                print("Regenerating...")
                try:

                    message= generate_message(diff=diff,config=config)
                    print(f"\n New suggested message: {message}\n")
                except RuntimeError as e:
                    print(f"Error: {e}")
                    sys.exit(1)
            case _:
                print("Invalid choice. Please enter y, n, e, or r.")


if __name__ == "__main__":
    run()
