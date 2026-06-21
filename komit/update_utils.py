# komit/update_utils.py
import importlib.metadata
import subprocess
import sys

from rich.console import Console

console = Console()


def check_for_updates():
    try:
        from komit import __version__

        latest = _get_latest_version()
        if latest != __version__:
            console.print(
                f"\n[bold yellow]!! New version available: v{latest}[/bold yellow] [dim](you have v{__version__})[/dim]"  # noqa: E501
            )  # noqa: E501
            console.print("[dim]   Use: komit update[/dim]\n")
    except Exception:
        pass


def uninstall() -> None:
    """Remove komit completely = pip, binary, git alias and config."""
    import os
    import shutil

    console.print("[bold red]Uninstalling komit...[/bold red]")
    method = _detect_install_method()
    # Remove git alias
    try:
        subprocess.run(["git", "config", "--global", "--unset", "alias.ai"], check=False)
        console.print("[green]Removed git alias[/green]")
    except Exception:
        pass

    # Remove config file
    config_path = os.path.expanduser("~/.config/komit")
    if os.path.exists(config_path):
        shutil.rmtree(config_path)
        console.print("[green]Removed ~/.config/komit[/green]")

    if sys.platform == "win32":
        windows_path = os.path.join(os.environ.get("LOCALAPPDATA", ""), "komit")
        if os.path.exists(windows_path):
            shutil.rmtree(windows_path)
            console.print(f"[green]Removed {windows_path}[/green]")
        try:
            import winreg

            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_ALL_ACCESS)
            current_path, _ = winreg.QueryValueEx(key, "Path")
            new_path = ";".join(p for p in current_path.split(";") if "komit" not in p)
            winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, new_path)
            winreg.CloseKey(key)
            console.print("[green]Removed from PATH[/green]")
        except Exception as e:
            console.print(f"[yellow]Could not remove from PATH: {e}[/yellow]")
    # Remove binary if installed via curl
    all_paths = ["~/.local/bin/komit", "/usr/local/bin/komit", "/opt/homebrew/bin/komit"]

    for p in all_paths:
        binary = os.path.expanduser(p)
        if os.path.exists(binary):
            try:
                subprocess.run(["sudo", "rm", "-f", binary], check=True)
                console.print(f"[green]Removed {binary}[/green]")
            except subprocess.CalledProcessError:
                console.print(f"[yellow]Failed to remove {binary} - try: sudo rm {binary}[/yellow]")
    # remove for pip
    if method == "pip":
        try:
            subprocess.run([sys.executable, "-m", "pip", "uninstall", "komit", "-y"], check=False)
            console.print("[green]Removed pip package[/green]")
        except subprocess.CalledProcessError:
            pass

    console.print("\n[bold red]komit uninstalled. Goodbye![/bold red]")


def _detect_install_method() -> str:
    import sys

    # 1. PyInstaller / bundled binary
    if getattr(sys, "frozen", False):
        return "binary"

    # 2. pip install (most reliable check)
    try:
        importlib.metadata.version("komit")
        return "pip"
    except importlib.metadata.PackageNotFoundError:
        pass

    # 3. fallback
    return "binary"


def _get_latest_version() -> str:
    import httpx

    # Use GitHub
    try:
        response = httpx.get(
            "https://api.github.com/repos/glemiu6/komit/releases/latest", timeout=2
        )
        data = response.json()
        if "tag_name" in data:
            return data["tag_name"].lstrip("v")
    except Exception:
        pass
    # Use the PyPI as a backup
    response = httpx.get("https://pypi.org/pypi/komit/json", timeout=2)
    return response.json()["info"]["version"]


def update():
    """Update the komit using CLI commands"""
    try:
        import importlib.util

        from komit import __version__

        latest = _get_latest_version()
        if latest == __version__:
            console.print("[bold green]Already up to date![/bold green]")
            return
        console.print(
            f"\n[bold yellow]!! New version available: v{latest}[/bold yellow] [dim](you have v{__version__})[/dim]"  # noqa: E501
        )  # noqa: E501
        console.print("[dim]   Use: komit update[/dim]\n")
        method = _detect_install_method()
        match method:
            case "pip":
                console.print("Detected pip installation, updating...")
                if importlib.util.find_spec("pip") is None:
                    console.print("pip not found, installing...")
                    subprocess.run([sys.executable, "-m", "ensurepip", "--upgrade"], check=True)
                subprocess.run(
                    [sys.executable, "-m", "pip", "install", "--upgrade", "komit"], check=True
                )  # noqa: E501
            case "binary":
                console.print("Detected binary installation, updating...")
                if sys.platform == "win32":
                    subprocess.run(
                        [
                            "powershell",
                            "-Command",
                            "irm https://raw.githubusercontent.com/glemiu6/komit/master/scripts/install.ps1 | iex",  # noqa: E501
                        ],  # noqa: E501
                        check=True,
                    )
                else:
                    result = subprocess.run(
                        [
                            "curl",
                            "-fsSL",
                            "https://raw.githubusercontent.com/glemiu6/komit/master/scripts/install.sh",
                        ],
                        capture_output=True,
                        check=True,
                    )
                    subprocess.run(["bash"], input=result.stdout, check=True)
            case _:
                console.print(
                    "[yellow]Could not detect installation method. Please update manually:[/yellow]"
                )  # noqa: E501
                console.print("  [cyan]pip install --upgrade komit[/cyan]")
                console.print(
                    "  [cyan]curl -fsSL https://raw.githubusercontent.com/glemiu6/komit/master/scripts/install.sh | sh[/cyan]"  # noqa: E501
                )  # noqa: E501
                console.print(
                    "  [cyan]irm https://raw.githubusercontent.com/glemiu6/komit/master/scripts/install.ps1 | iex[/cyan]"  # noqa: E501
                )  # noqa: E501
        console.print(
            "[bold green]Update complete! Restart your terminal to use the latest version.[/bold green]"  # noqa: E501
        )  # noqa: E501
    except Exception as e:
        console.print(f"[bold red]Failed to update: {e}[/bold red]")
        sys.exit(1)


if __name__ == "__main__":
    print(_get_latest_version())
