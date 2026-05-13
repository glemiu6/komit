#!/usr/bin/env python3
#komit/main.py
import subprocess
import sys
import argparse
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from komit.git_utils import get_staged_files,get_staged_diff,is_git_repo,commit,commit_with_editor
from komit.generator import generate_message,STYLES
from komit.komitconfig import KomitConfig
from komit.update_utils import check_for_updates,update,uninstall
from komit import __version__
from komit.config_utils import init_config

def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        prog="komit",
        description="AI-powered git commit message generator using local LLMs via Ollama."
    )

    #add flag for style
    parser.add_argument(
        '-s',
        '--style',
        choices=list(STYLES.keys()),
        default=None,
        help="Choose the style of the commit message (default: conventional)."
    )
    #add flag for model
    parser.add_argument(
        '-m',
        '--model',
        default=None,
        help="Choose the model (default: qwen2.5:7b)."
    )
    #add flag for url
    parser.add_argument(
        '--ollama-url',
        '-u',
        default=None,
        help="Choose the URL of the Ollama (default: http://localhost:11434)."
    )
    #add flag for max difference length
    parser.add_argument(
        '--max_diff',
        default=None,
        type=int,
        help="Choose the maximum diff length (default: 4000)."
    )

    #add flag for version
    parser.add_argument('--version',action='version',
                        version=f"{__version__}",
                        help="Version of the package")
    #flag to test the commits without executing
    parser.add_argument(
        '--dry-run',
        '-dr',
        action='store_true',
        help="Don't actually commit the changes."
    )
    #flag for passing config file (if not , use default values)
    parser.add_argument(
        '--config',
        type=str,
        help="Path to custom config file"
    )
    # flag for timeout in LLM
    parser.add_argument(
        '--timeout',
        type = int,
        default = None,
        help='LLM request timeout in seconds (default: 60)'
    )
    #subparser for action commands
    subparser = parser.add_subparsers(dest='command')
    # flag from the action komit init
    subparser.add_parser(
        'init',
        help="Create a config file"
    )
    subparser.add_parser(
        'update',
        help="Update komit to the latest version"
    )
    subparser.add_parser(
        'uninstall',
        help="Uninstall komit"
    )
    return parser.parse_args(argv)
def run():
    console = Console()
    args = parse_args()

    if args.command == 'init':
        init_config()
        return
    if args.command == 'uninstall':
        uninstall()
        return
    if args.command == 'update':
        update()
        return
    check_for_updates()
    if not is_git_repo():
        console.print("Not a git repository",style="yellow")
        sys.exit(1)
    diff = get_staged_diff()
    if not diff:
        console.print("No staged changes. Run 'git add' first.",style="yellow")
        sys.exit(1)
    files= get_staged_files()
    files_text = "\n".join(f" [cyan]•[/cyan] {f}" for f in files)
    console.print(Panel(files_text,title=f"Staged files ({len(files)})",border_style="blue"))
    config = KomitConfig.from_sources(args)
    console.print(f"Model: [cyan]{config.model}[/cyan] · Style: [cyan]{config.style}[/cyan]",style="dim")
    try:
        with console.status("Generating commit message...", spinner="dots"):
            message= generate_message(diff=diff,config=config)
        if not message or not isinstance(message, str):
            console.print("Invalid response from generator")
            sys.exit(1)
    except RuntimeError as e:
        console.print(f"Error: {e}",style="bold red")
        sys.exit(1)
    console.print(Panel(message,title="Suggested commit message",border_style="green"))
    if args.dry_run:
        console.print("Running in dry-run mode, no actual changes will be made.",style='yellow')
        sys.exit(0)
    while True:
        choice= input("\nUse this message? (y/n/e to edit/r to regenerate): ").strip().lower()
        match choice :
            case 'y':
                try:
                    commit(message)
                    console.print("✓ Committed!",style="bold green")
                except subprocess.CalledProcessError as e:
                    console.print(f"Commit failed: {e}",style="bold red")
                    sys.exit(1)
                break
            case 'n':
                console.print("✗ Commit cancelled!",style="red")
                break
            case 'e':
                try:
                    commit_with_editor(message)
                except subprocess.CalledProcessError as e:
                    console.print(f"Commit failed: {e}",style="bold red")
                    sys.exit(1)
                break
            case 'r':

                try:
                    with console.status("Regenerating...", spinner='dots'):
                        message= generate_message(diff=diff,config=config)
                    console.print(Panel(message,title= "New suggested message:",border_style="green"))
                except RuntimeError as e:
                    console.print(f"Error: {e}")
                    sys.exit(1)
            case _:
                console.print("Invalid choice. Please enter y, n, e, or r.",style="yellow")


if __name__ == "__main__":
    run()
