#!/usr/bin/env python3
#komit/main.py
import subprocess
import sys
from komit.git_utils import get_staged_files,get_staged_diff,is_git_repo,commit,commit_with_editor
from komit.generator import generate_message
from komit.komitconfig import KomitConfig

def run():
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

    try:
        config = KomitConfig()
        message= generate_message(diff=diff,config=config)
    except RuntimeError as e:
        print(f"Error: {e}")
        sys.exit(1)
    print(f"\nSuggested message: {message}")
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
