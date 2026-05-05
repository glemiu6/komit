#komit/update_utils.py
import subprocess
import sys
import importlib.metadata


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
            print(f"    Use: komit update\n")
    except Exception:
        pass

def uninstall()->None:
    """Remove komit completely = pip, binary, git aliar and config."""
    import shutil
    import os
    print("Uninstalling komit...")
    #Remove git alias
    try:
        subprocess.run(['git','config','--global','--unset','alias.ai'],check=False)
        print("Removed git alias")
    except Exception:
        pass

    #Remove config file
    config_path = os.path.expanduser("~/.config/komit")
    if os.path.exists(config_path):
        shutil.rmtree(config_path)
        print("Removed ~/.config/komit")

    #Remove binary if installed via curl
    all_paths = [
       "~/.local/bin/komit",
       "/usr/local/bin/komit",
       "/opt/homebrew/bin/komit"
   ]

    for p in all_paths:
        binary= os.path.expanduser(p)
        if os.path.exists(binary):
            try:
                subprocess.run(['sudo','rm','-f',binary],check=True)
                print(f"Removed {binary}")
            except subprocess.CalledProcessError:
                print(f"Failed to remove {binary}: Try : sudo rm {binary}")
    #remove for pip
    try:
        subprocess.run([sys.executable,'-m','pip','uninstall','komit','-y'],check=True)
        print("Removed pip package")
    except subprocess.CalledProcessError:
        pass

    print("\nkomit uninstalled. Goodbye!")

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

def update():
    """Update the komit using CLI commands"""
    try:
        import httpx
        from komit import __version__

        response= httpx.get(
            "https://api.github.com/repos/glemiu6/komit/releases/latest",
            timeout=2
        )
        latest= response.json()["tag_name"].lstrip("v")
        if latest == __version__:
            print("Already up to date!")
            return
        print(f"Updating komit: v{__version__} -> v{latest}")
        method = _detect_install_method()
        match method:
            case "pip":
                print("Detected pip installation, updating...")
                try:
                    import pip
                except ImportError:
                    print("pip not found, installing...")
                    subprocess.run([sys.executable, "-m", "ensurepip", "--upgrade"], check=True)
                subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "komit"], check=True)
            case "binary":
                print("Detected binary installation, updating...")
                subprocess.run(["curl", "-fsSL", "https://raw.githubusercontent.com/glemiu6/komit/main/install.sh", "|", "sh"], check=True,shell=True)
            case _:
                print("Could not detect installation method.")
                print("Please update manually.")
                print("     pip install --upgrade komit")
                print("     or")
                print("     curl -fsSL https://raw.githubusercontent.com/glemiu6/komit/main/install.sh | sh")
        print("Update complete! Restart your terminal to use the latest version.")
    except Exception as e:
        print(f"Failed to update: {e}")
        sys.exit(1)