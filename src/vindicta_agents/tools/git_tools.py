import subprocess
import os
from .filesystem import _validate_path

def run_git_command(repo_path: str, args: list) -> str:
    """Runs a git command in the specified repository path."""
    try:
        abs_path = _validate_path(repo_path)
        if not os.path.isdir(os.path.join(abs_path, ".git")):
             return f"Error: {repo_path} is not a git repository."

        result = subprocess.run(
            ["git"] + args,
            cwd=abs_path,
            capture_output=True,
            text=True,
            check=False 
        )
        if result.returncode != 0:
            return f"Git Error ({result.returncode}): {result.stderr}"
        return result.stdout.strip()
    except Exception as e:
        return f"Execution Error: {str(e)}"

def checkout_branch(repo_path: str, branch_name: str, create: bool = False) -> str:
    """Checkouts a branch, optionally creating it."""
    args = ["checkout"]
    if create:
        args.append("-b")
    args.append(branch_name)
    return run_git_command(repo_path, args)

def commit_changes(repo_path: str, message: str, files: list = ["."]) -> str:
    """Stages files and commits them."""
    # Stage
    stage_res = run_git_command(repo_path, ["add"] + files)
    if stage_res.startswith("Error") or stage_res.startswith("Git Error"):
        return stage_res
    
    # Commit
    return run_git_command(repo_path, ["commit", "-m", message])

def push_changes(repo_path: str, branch_name: str, remote: str = "origin") -> str:
    """Pushes changes to remote."""
    return run_git_command(repo_path, ["push", remote, branch_name])
    
def get_current_branch(repo_path: str) -> str:
    return run_git_command(repo_path, ["rev-parse", "--abbrev-ref", "HEAD"])
