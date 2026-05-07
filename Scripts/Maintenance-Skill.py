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

from os import remove as osRemove
from time import time as timeTime
from pathlib import Path
from sys import argv as sysArgv

# ### CONFIGURATIONS ###

SCRIPT_DIR = Path(__file__).resolve().parent
# core-kms-brain/Scripts -> parent is core-kms-brain -> parent is root
WORKSPACE_DIR = SCRIPT_DIR.parents[1]

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
