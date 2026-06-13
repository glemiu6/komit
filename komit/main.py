#!/usr/bin/env python3
#komit/main.py
import subprocess
import sys
import argparse
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

from komit.git_utils import get_staged_files,get_staged_diff,is_git_repo,commit,commit_with_editor,get_current_branch
from komit.generator import generate_message,STYLES
from komit.komitconfig import KomitConfig
from komit.update_utils import check_for_updates, update, uninstall
from komit import __version__
from komit.config_utils import init_config

def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        prog="komit",
        description="AI-powered git commit message generator using local LLMs via Ollama.",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""
        Examples:
        $ komit --style conventional --dry-run
        $ komit --model llama3
        $ komit init
        """
    )

    config_group = parser.add_argument_group("Configuration & LLM Options")

    #add flag for style
    config_group.add_argument(
        '-s','--style',
        choices=list(STYLES.keys()),
        default=None,
        metavar="<type>",
        help="Choose the style of the commit message (default: conventional)."
    )
    #add flag for model
    config_group.add_argument(
        '-m','--model',
        default=None,
        metavar="<name>",
        help="Choose the model (default: qwen2.5:7b)."
    )
    #add flag for url
    config_group.add_argument(
        '--ollama-url','-u',
        default=None,
        metavar="<url>",
        help="Choose the URL of the Ollama (default: http://localhost:11434)."
    )
    #add flag for max difference length
    config_group.add_argument(
        '--max_diff',
        default=None,
        type=int,
        metavar="<len>",
        help="Choose the maximum diff length (default: 4000)."
    )
    # flag for passing config file (if not , use default values)
    config_group.add_argument(
        '--config',
        type=str,
        metavar="<path>",
        help="Path to custom configuration TOML file"
    )
    # flag for timeout in LLM
    config_group.add_argument(
        '--timeout',
        type=int,
        default=None,
        metavar="<sec>",
        help='LLM request timeout in seconds (default: 60)'
    )
    #flag for branch detection
    config_group.add_argument(
        '--include_branch_name',
        '-ib',
        type=bool,
        default=None,
        metavar="<bool>",
        help='Include branch name in commit message (default: True)'
    )

    execution_group = parser.add_argument_group("Execution Options")

    #add flag for version
    execution_group.add_argument('--version',action='version',
                        version=f"{__version__}",
                        help="Version of the package")
    #flag to test the commits without executing
    execution_group.add_argument(
        '--dry-run','-dr',
        action='store_true',
        help="Don't actually commit the changes."
    )
    #flag for explaining the changes without commiting
    execution_group.add_argument(
        '--explain',
        action="store_true",
        help="Explain staged changes without committing."
    )
    execution_group.add_argument(
        '--deep',
        action="store_true",
        help="Summarize each file separately for better commit messages on large diffs (slower)."
    )

    #flag for enable hook mode
    execution_group.add_argument(
        '--hook-mode',
        action="store_true",
        help=argparse.SUPPRESS
    )

    execution_group.add_argument(
        '--msg-file',
        default=None,
        metavar="<path>",
        help=argparse.SUPPRESS
    )
    #subparser for action commands
    subparser = parser.add_subparsers(
        title="Available Maintenance Commands",
        description="Run utility routines instead of generating a commit message.",
        dest='command',
        metavar="<command>"
    )
    # flag from the action komit init
    subparser.add_parser(
        'init',
        help="Create a fresh base configuration file."
    )
    subparser.add_parser(
        'update',
        help="Pull down the latest version updates."
    )
    subparser.add_parser(
        'uninstall',
        help="Safely remove komit from your system."
    )
    subparser.add_parser(
        'install-hook',
        help="Integrate komit seamlessly as an automated Git hook."
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
    branch_name = get_current_branch() if config.include_branch_name else ""
    console.print(f"Branch name: [blue]{branch_name}[/blue]",style="dim")
    console.print(f"Model: [cyan]{config.model}[/cyan] · Style: [cyan]{config.style}[/cyan]",style="dim")
    if args.explain:
        from komit.generator import explain_changes
        with console.status("Explaining changes...",spinner="dots"):
            explanation = explain_changes(diff=diff,config=config)
        console.print(Panel(explanation,title="What changed",border_style="cyan"))
        sys.exit(0)
    try:
        status_msg = "Generating commit message (deep mode)..." if args.deep else "Generate commit message..."
        with console.status(status_msg, spinner="dots"):
            message,truncated= generate_message(diff=diff,config=config,branch_info=branch_name,deep=args.deep)
            if truncated:
                console.print(f"[yellow]!! Large files were truncated: {', '.join(truncated)}[/yellow]")
                console.print("[dim]Use --deep for full analysis or increase the --max_diff[/dim]")

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

        choice= Prompt.ask(
            "\n[bold cyan]»[/bold cyan] Choose an action: ([green]y[/green])es, ([red]n[/red])o, ([yellow]e[/yellow])dit, ([magenta]r[/magenta])egenerate",
            choices=["y","n","e","r"],
            show_choices=False,
            default="y"
        )
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
                    break
                except subprocess.CalledProcessError as e:
                    console.print(f"Commit failed: {e}",style="bold red")
                    sys.exit(1)
            case 'r':

                try:
                    with console.status("Regenerating...", spinner='dots'):
                        message,truncated= generate_message(diff=diff,config=config,branch_info=branch_name)
                    console.print(Panel(message,title= "New suggested message:",border_style="green"))
                except RuntimeError as e:
                    console.print(f"Error: {e}")
                    sys.exit(1)


if __name__ == "__main__":
    run()
