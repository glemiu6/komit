#! /usr/bin/env python3
#komit/main.py
import sys
from komit.git_utils import get_stage_files,get_stage_diff,is_git_repo,commit,commit_with_editor
from komit.generator import generate_message
from komit.config import Config

def run():
    if not is_git_repo():
        print("Not a git repository")
        sys.exit(1)
    diff = get_stage_diff()
    if not diff:
        print("No staged changes. Run 'git add' first.")
        sys.exit(1)
    files= get_stage_files()
    print(f"\nStage files {len(files)}:")
    for f in files:
        print(f"  - {f}")
    print("\nGenerating commit message...")

    try:
        config = Config()
        message= generate_message(diff=diff,config=config)
    except RuntimeError as e:
        print(f"Error: {e}")
        sys.exit(1)
    print(f"\nSuggested message: {message}")
    while True:
        choice= input("\nUse this message? (y/n/e to edit/r to regenerate): )").strip().lower()
        match(choice):
            case 'y':
                commit(message)
                print("Commited!")
                break
            case 'n':
                print("Commit cancelled!")
                break
            case 'e':
                commit_with_editor(message)
                break
            case 'r':
                print("Regenerating...")
                message= generate_message(diff=diff,config=config)
                print(f"\n New suggested message: {message}\n")

if __name__ == "__main__":
    run()
