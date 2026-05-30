#komit/git_utils.py
import subprocess
import re

def get_staged_diff() -> str:
    result = subprocess.run(['git', 'diff', '--staged'], capture_output=True,text=True,encoding='utf-8',errors="replace")
    return result.stdout

def get_staged_files() -> list[str]:
    result = subprocess.run(['git', 'diff', '--staged', '--name-only'], capture_output=True,text=True,encoding='utf-8')
    return [f for f in result.stdout.strip().split('\n') if f]
def get_changed_files() -> list[str]:
    result = subprocess.run(['git', 'diff','--cached', '--name-only'], capture_output=True,text=True,encoding='utf-8',check=True)
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

def get_recent_commits(n:int=3)->str:
    result = subprocess.run(
        ['git','log',f'-{n}','--oneline'],
        check=True,
        text=True,
        encoding='utf-8',
        capture_output=True
    )
    return result.stdout.strip()

def is_git_repo():
    result = subprocess.run(['git','rev-parse','--is-inside-work-tree'],capture_output=True,text=True,encoding='utf-8')
    return result.returncode == 0

def parse_branch_name(branch_name:str)->dict:
    if not branch_name:
        return {"type":None,"scope":None}

    branch_name = branch_name.strip().lower()

    match =re.match(r"^([a-z]+)[\/\-]([a-z0-9\-_]+)",branch_name)
    if match:
        inferred_type = match.group(1)
        inferred_scope =match.group(2)
        valid_types = ["feat","fix","chore","docs","style","refactor","test","ci","perf"]
        if inferred_type in valid_types:
            return {"type":inferred_type,"scope":inferred_scope}
    return {"type":None,"scope":None}
