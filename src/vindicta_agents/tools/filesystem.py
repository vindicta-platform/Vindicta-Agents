import os
import difflib
from typing import List, Optional, Dict, Any

# Safety mechanism: only allow operations within the platform root
PLATFORM_ROOT = os.environ.get("VINDICTA_PLATFORM_ROOT") or os.path.abspath(os.path.join(os.getcwd(), ".."))

def _validate_path(path: str) -> str:
    """Ensures the path is absolute and within the platform root."""
    abs_path = os.path.abspath(path)
    if not abs_path.startswith(PLATFORM_ROOT):
        # Allow if it's within the current CWD (Vindicta-Agents) as fallback
        cwd = os.getcwd()
        if not abs_path.startswith(cwd):
             raise ValueError(f"Access denied: {path} is outside platform root {PLATFORM_ROOT}")
    return abs_path

def read_file(path: str) -> str:
    """Reads a file and returns its content."""
    try:
        abs_path = _validate_path(path)
        with open(abs_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file {path}: {str(e)}"

def write_file(path: str, content: str) -> str:
    """Writes content to a file. Overwrites if exists."""
    try:
        abs_path = _validate_path(path)
        os.makedirs(os.path.dirname(abs_path), exist_ok=True)
        with open(abs_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"Successfully wrote to {path}"
    except Exception as e:
        return f"Error writing file {path}: {str(e)}"

def list_dir(path: str) -> str:
    """Lists files and directories in a path."""
    try:
        abs_path = _validate_path(path)
        if not os.path.exists(abs_path):
             return f"Path does not exist: {path}"
        
        items = os.listdir(abs_path)
        return "\n".join(items)
    except Exception as e:
        return f"Error listing directory {path}: {str(e)}"

def file_diff(path: str, new_content: str) -> str:
    """Returns a diff between existing file content and new content."""
    try:
        current_content = read_file(path)
        if current_content.startswith("Error"):
            return f"Cannot diff, file error: {current_content}"
            
        diff = difflib.unified_diff(
            current_content.splitlines(), 
            new_content.splitlines(), 
            fromfile=path, 
            tofile="new_content",
            lineterm=""
        )
        return "\n".join(diff)
    except Exception as e:
        return f"Error generating diff for {path}: {str(e)}"
