#komit/git_utils.py
import subprocess

def get_staged_diff() -> str:
    result = subprocess.run(['git', 'diff', '--staged'], capture_output=True,text=True,encoding='utf-8',errors="replace")
    return result.stdout

def get_staged_files() -> list[str]:
    result = subprocess.run(['git', 'diff', '--staged', '--name-only'], capture_output=True,text=True,encoding='utf-8')
    return [f for f in result.stdout.strip().split('\n') if f]

def commit(message:str):
    subprocess.run(
        ['git','commit','-m',message],check=True,encoding='utf-8'
    )

def commit_with_editor(message:str):
    subprocess.run(
        ['git','commit','-m',message,'-e'],
        check=True,
        text=True
        ,encoding='utf-8'
    )
def get_current_branch():
    result = subprocess.run(
        ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
        check=True,
        text=True,
        encoding='utf-8',
        capture_output=True
    )
    return result.stdout.strip()

def is_git_repo():
    result = subprocess.run(['git','rev-parse','--is-inside-work-tree'],capture_output=True,text=True,encoding='utf-8')
    return result.returncode == 0