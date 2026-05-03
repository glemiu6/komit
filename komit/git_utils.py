#komit/git_utils.py
import subprocess

def get_stage_diff() ->str:
    result = subprocess.run(['git','diff','--staged'],capture_output=True,text=True)
    return result.stdout

def get_stage_files()->list[str]:
    result = subprocess.run(['git','diff','--staged','--name-only'],capture_output=True,text=True)
    return [f for f in result.stdout.strip().split('\n') if f]

def commit(message:str):
    subprocess.run(
        ['git','commit','-m',message]
    )

def commit_with_editor(message:str):
    subprocess.run(
        ['git','commit','-m',message,'-e']
    )

def is_git_repo():
    result = subprocess.run(['git','rev-parse','--is-inside-work-tree'],capture_output=True,text=True)
    return result.returncode == 0