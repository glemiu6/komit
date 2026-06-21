# komit/git_utils.py
import re
import subprocess


def get_staged_diff() -> str:
    result = subprocess.run(
        ["git", "diff", "--staged"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )  # noqa: E501
    return result.stdout


def get_staged_files() -> list[str]:
    result = subprocess.run(
        ["git", "diff", "--staged", "--name-only"], capture_output=True, text=True, encoding="utf-8"
    )  # noqa: E501
    return [f for f in result.stdout.strip().split("\n") if f]


def get_changed_files() -> list[str]:
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=True,
    )  # noqa: E501
    return [f for f in result.stdout.strip().split("\n") if f]


def commit(message: str) -> None:
    subprocess.run(["git", "commit", "-m", message], check=True, encoding="utf-8")


def commit_with_editor(message: str) -> None:
    subprocess.run(["git", "commit", "-m", message, "-e"], check=True, text=True, encoding="utf-8")


def get_current_branch() -> str:
    result = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        check=True,
        text=True,
        encoding="utf-8",
        capture_output=True,
    )
    return result.stdout.strip()


def get_recent_commits(n: int = 3) -> str:
    result = subprocess.run(
        ["git", "log", f"-{n}", "--oneline"],
        check=True,
        text=True,
        encoding="utf-8",
        capture_output=True,
    )
    return result.stdout.strip()


def is_git_repo() -> bool:
    result = subprocess.run(
        ["git", "rev-parse", "--is-inside-work-tree"],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )  # noqa: E501
    return result.returncode == 0


def parse_branch_name(branch_name: str) -> dict:
    if not branch_name:
        return {"type": None, "scope": None}

    branch_name = branch_name.strip().lower()

    match = re.match(r"^([a-z]+)[/\-]([a-z0-9\-_]+)", branch_name)
    if match:
        inferred_type = match.group(1)
        inferred_scope = match.group(2)
        valid_types = ["feat", "fix", "chore", "docs", "style", "refactor", "test", "ci", "perf"]
        if inferred_type in valid_types:
            return {"type": inferred_type, "scope": inferred_scope}
    return {"type": None, "scope": None}


def split_diff_by_file(diff: str) -> dict[str, str]:
    chunks = {}
    parts = diff.split("diff --git ")
    for part in parts:
        if not part.strip():
            continue
        first_line = part.split("\n")[0]
        filename = first_line.split(" b/")[-1].strip()
        chunks[filename] = "diff --git " + part
    return chunks


def allocate_diff(diff: str, max_length: int) -> tuple[str, list[str]]:
    DOC_EXTENSION = {".md", ".txt", ".rst", ".changelog"}
    import os

    file_chunk = split_diff_by_file(diff)
    if not file_chunk:
        truncated = diff[:max_length] + "\n... (truncated)" if len(diff) > max_length else diff
        return truncated, ["(unknown file)"] if len(diff) > max_length else []

    process = []
    truncated_files = []
    for filename, chunk in file_chunk.items():
        ext = os.path.splitext(filename)[1].lower()
        if ext in DOC_EXTENSION:
            limit = 300
        else:
            limit = max_length // max(1, len(file_chunk))

        if len(chunk) <= limit:
            process.append(chunk)
        else:
            process.append(chunk[:limit] + "\n... (truncated)")
            truncated_files.append(filename)
    return "\n".join(process), truncated_files
