#komit/update_utils.py
import subprocess
import sys


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
            print(f"    pip users: komit-update")
            print(f"    binary users: komit-update-binary\n")
    except Exception:
        pass

#update for when using pip install komit
def update_binary()->None:
    """Update komit via install script - use this if you installed with curl."""
    print("Updating komit binary...")
    try:
        curl = subprocess.run(["curl","-fsSL","https://raw.githubusercontent.com/glemiu6/komit/master/scripts/install.sh"],
                                capture_output=True,text=True,check=True)
        subprocess.run(['bash'],input=curl.stdout,check=True)
        print("Done! Restart your terminal to use the new version.")
    except subprocess.CalledProcessError as e:
        print(f"Update failed: {e}")
        print("Try manually: curl -fsSL https://raw.githubusercontent.com/glemiu6/komit/master/scripts/install.sh | bash")
        sys.exit(1)
def update_pip()->None:
    """Update komit via pip - use this if you installed with pip."""
    print("Updating komit via pip...")
    try:
        subprocess.run([sys.executable,'-m','pip','install','--upgrade','komit'],check=True)
        print("Done! Restart your terminal to use the new version.")
    except subprocess.CalledProcessError as e:
        print(f"Update failed: {e}")
        sys.exit(1)

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
    binary ="/usr/local/bin/komit"
    updater = "/usr/local/bin/komit-update-binary"
    for path in [binary, updater]:
        if os.path.exists(path):
            try:
                subprocess.run(['sudo','rm','-f',path],check=True)
                print(f"Removed {path}")
            except subprocess.CalledProcessError:
                print(f"Failed to remove {path}: Try : sudo rm {path}")
    #remove for pip
    try:
        subprocess.run([sys.executable,'-m','pip','uninstall','komit','-y'],check=True)
        print("Removed pip package")
    except subprocess.CalledProcessError:
        pass

    print("\nkomit uninstall. Goodbye!")