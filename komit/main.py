#!/usr/bin/env python3
#komit/main.py
import subprocess
import sys
import argparse
from komit.git_utils import get_staged_files,get_staged_diff,is_git_repo,commit,commit_with_editor
from komit.generator import generate_message,STYLES
from komit.komitconfig import KomitConfig
from komit.update_utils import update,check_for_updates

def parse_args():
    parser = argparse.ArgumentParser(
        prog="komit",
        description="AI-powered git commit message generator using local LLMs via Ollama."
    )
    #add update subcommand
    subparser = parser.add_subparsers(dest='command')
    subparser.add_parser("update",help="Update komit to the latest version")
    #add flag for style
    parser.add_argument(
        '-s',
        '--style',
        choices=list(STYLES.keys()),
        default='conventional',
        help="Choose the style of the commit message (default: conventional)."
    )
    #add flag for model
    parser.add_argument(
        '-m',
        '--model',
        default='qwen2.5:7b',
        help="Choose the model (default: qwen2.5:7b)."
    )
    #add flag for url
    parser.add_argument(
        '--ollama-url',
        '-u',
        default='http://localhost:11434',
        help="Choose the URL of the Ollama (default: http://localhost:11434)."
    )
    #add flag for max difference length
    parser.add_argument(
        '--max_diff',
        default=4000,
        type=int,
        help="Choose the maximum diff length (default: 4000)."
    )
    return parser.parse_args()
def run():
    args = parse_args()
    if args.command == 'update':
        update()
        return
    check_for_updates()
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
