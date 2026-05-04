#komit/update_utils.py
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

#update for when using pip install komit
def update()->None:
    print("Updating komit...")
    result = subprocess.run(["curl","-fsSL","https://raw.githubusercontent.com/glemiu6/komit/master/scripts/install.sh"],capture_output=True,text=True)
    subprocess.run(['bash'],input=result.stdout)
    print("Done!")
