#!/usr/bin/env python
# coding:utf-8
"""
ESSENTIAL PROCESS:
Performs routine maintenance tasks across the ecosystem, specifically 
purging stale AI-Session-State.md files to prevent context bloat.

DATA FLOW:
1. Scans all directories in the workspace root for AI-Session-State.md.
2. Checks the last modification time of each file.
3. Deletes files older than 30 days (excluding the central obsidian-brain state).

KEY PARAMETERS:
- WORKSPACE_DIR: The root directory containing all brain repositories.
- state_file: Target file name for the purge operation.
"""
import os, sys
# Ensure we are running inside the virtual environment
_venv_dir = os.path.dirname(os.path.abspath(__file__))
while _venv_dir and _venv_dir != '/' and not os.path.exists(os.path.join(_venv_dir, ".venv")):
    _parent = os.path.dirname(_venv_dir)
    if _parent == _venv_dir:
        break
    _venv_dir = _parent
_venv_python = os.path.join(_venv_dir, ".venv", "Scripts", "python.exe") if os.name == "nt" else os.path.join(_venv_dir, ".venv", "bin", "python3")
if os.path.exists(_venv_python):
    try:
        if not os.path.samefile(sys.executable, _venv_python):
            os.execl(_venv_python, _venv_python, *sys.argv)
    except OSError:
        pass


from os import remove as osRemove
from time import time as timeTime
from pathlib import Path
from sys import argv as sysArgv

# ### CONFIGURATIONS ###

def _find_workspace_root() -> Path:
    """
    Walk up from this script's location until we find the workspace root.
    """
    current = Path(__file__).resolve().parent
    for parent in [current] + list(current.parents):
        if (parent / "Bastien-Antigravity.code-workspace").exists():
            return parent
        if (parent / "obsidian-brain").is_dir() and (parent / "fleet-operation-brain").is_dir():
            return parent
    return Path(__file__).resolve().parents[1]

WORKSPACE_DIR = _find_workspace_root()

# -----------------------------------------------------------------------------------------------

def purge_stale_state() -> None:
    """
    Identifies and removes AI-Session-State.md files that haven't been touched in 30 days.
    """
    print("[*] Checking for stale state files (older than 30 days)...")
    now = timeTime()
    count = 0
    for state_file in WORKSPACE_DIR.rglob("AI-Session-State.md"):
        # Don't delete the central one in obsidian-brain
        if "obsidian-brain" in str(state_file): 
            continue
        if state_file.stat().st_mtime < now - 30 * 86400:
            osRemove(state_file)
            print("    Deleted stale state: {0}".format(state_file))
            count += 1
    if count == 0:
        print("    No stale state files found.")

# -----------------------------------------------------------------------------------------------

def main() -> None:
    """
    Orchestrates the maintenance operations.
    """
    print("Starting Maintenance Skill (Purger Mode)...")
    purge_stale_state()
    print("Maintenance complete.")

# -----------------------------------------------------------------------------------------------

if __name__ == "__main__":
    if len(sysArgv) > 1 and sysArgv[1] == "purge":
        main()
    else:
        print("Usage: python Maintenance-Skill.py purge")
