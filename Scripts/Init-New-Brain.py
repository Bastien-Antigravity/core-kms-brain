#!/usr/bin/env python
# coding:utf-8
"""
ESSENTIAL PROCESS:
Resets and initializes a new AI Brain environment by updating project 
variables, clearing the task inbox, and resetting session state.

DATA FLOW:
1. Inputs a new ecosystem name via CLI.
2. Updates Project-Variables.md with the new name.
3. Deletes all .md files in the Inbox folder (excluding templates).
4. Reinitializes AI-Session-State.md with a fresh header.

KEY PARAMETERS:
- ecosystem_name: The name of the new project being initialized.
"""

from os import remove as osRemove
from os.path import dirname as osPathDirname, abspath as osPathAbspath, join as osPathJoin, basename as osPathBasename
from glob import glob as globGlob
from sys import argv as sysArgv, exit as sysExit

# -----------------------------------------------------------------------------------------------

def _find_workspace_root() -> str:
    """
    Walk up from this script's location until we find the workspace root.
    """
    current = osPathDirname(osPathAbspath(__file__))
    while current != osPathDirname(current):
        if osPathExists(osPathJoin(current, "Bastien-Antigravity.code-workspace")):
            return current
        if osPathExists(osPathJoin(current, "obsidian-brain")) and osPathExists(osPathJoin(current, "fleet-operation-brain")):
            return current
        current = osPathDirname(current)
    return osPathDirname(osPathDirname(osPathAbspath(__file__)))

def init_brain(ecosystem_name: str) -> None:
    """
    Performs the initialization sequence for a fresh brain ecosystem.
    """
    print("Initializing new AI Brain for: {0}".format(ecosystem_name))
    
    wrapper_dir = _find_workspace_root()
    
    # Corrected paths for the actual Bastien-Antigravity structure
    obsidian_dir = osPathJoin(wrapper_dir, "obsidian-brain")
    project_vars_path = osPathJoin(obsidian_dir, "00-AI-Orchestration", "Project-Variables.md")
    inbox_dir = osPathJoin(obsidian_dir, "10-State-and-Tasks", "Inbox")
    session_state_path = osPathJoin(obsidian_dir, "00-AI-Orchestration", "AI-Session-State.md")
    
    # 1. Update Project Variables
    try:
        with open(project_vars_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        with open(project_vars_path, 'w', encoding='utf-8') as f:
            for line in lines:
                if line.startswith('ecosystem_name:'):
                    f.write('ecosystem_name: "{0}"\n'.format(ecosystem_name))
                else:
                    f.write(line)
        print("[-] Updated Project-Variables.md")
    except Exception as e:
        print("[!] Error updating Project-Variables: {0}".format(e))

    # 2. Clear Inbox
    try:
        for file in globGlob(osPathJoin(inbox_dir, "*.md")):
            osRemove(file)
            print("[-] Deleted old task: {0}".format(osPathBasename(file)))
    except Exception as e:
        print("[!] Error clearing Inbox: {0}".format(e))

    # 3. Clear Session State
    try:
        with open(session_state_path, 'w', encoding='utf-8') as f:
            f.write("# Central AI Session State\n\n*Brain Initialized. Ready for tasks.*")
        print("[-] Cleared AI-Session-State.md")
    except Exception as e:
        print("[!] Error clearing Session State: {0}".format(e))
        
    print("\n[SUCCESS] Brain successfully initialized! You can now write your Idea Pitch.")

# -----------------------------------------------------------------------------------------------

if __name__ == "__main__":
    if len(sysArgv) < 2:
        print("Usage: python Init-New-Brain.py <New-Ecosystem-Name>")
        sysExit(1)
    init_brain(sysArgv[1])
