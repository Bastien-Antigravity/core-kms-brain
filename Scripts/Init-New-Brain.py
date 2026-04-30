#!/usr/bin/env python
# coding:utf-8

from os.path import dirname as osPathDirname, abspath as osPathAbspath, join as osPathJoin, basename as osPathBasename
from glob import glob as globGlob
from sys import argv as sysArgv, exit as sysExit
from os import remove as osRemove
from typing import List

# -----------------------------------------------------------------------------------------------

def init_brain(ecosystem_name: str) -> None:
    print(f"Initializing new AI Brain for: {ecosystem_name}")
    
    core_dir = osPathDirname(osPathDirname(osPathAbspath(__file__)))
    wrapper_dir = osPathDirname(core_dir)
    
    project_vars_path = osPathJoin(wrapper_dir, "Project-Variables.md")
    inbox_dir = osPathJoin(wrapper_dir, "state-and-tasks", "Inbox")
    session_state_path = osPathJoin(wrapper_dir, "AI-Session-State.md")
    
    # 1. Update Project Variables
    try:
        with open(project_vars_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        with open(project_vars_path, 'w', encoding='utf-8') as f:
            for line in lines:
                if line.startswith('ecosystem_name:'):
                    f.write(f'ecosystem_name: "{ecosystem_name}"\n')
                else:
                    f.write(line)
        print("[-] Updated Project-Variables.md")
    except Exception as e:
        print(f"[!] Error updating Project-Variables: {e}")

    # 2. Clear Inbox (except Templates)
    try:
        for file in globGlob(osPathJoin(inbox_dir, "*.md")):
            osRemove(file)
            print(f"[-] Deleted old task: {osPathBasename(file)}")
    except Exception as e:
        print(f"[!] Error clearing Inbox: {e}")

    # 3. Clear Session State
    try:
        with open(session_state_path, 'w', encoding='utf-8') as f:
            f.write("# Central AI Session State\n\n*Brain Initialized. Ready for tasks.*")
        print("[-] Cleared AI-Session-State.md")
    except Exception as e:
        print(f"[!] Error clearing Session State: {e}")
        
    print("\n[SUCCESS] Brain successfully initialized! You can now write your Idea Pitch.")

# -----------------------------------------------------------------------------------------------

if __name__ == "__main__":
    if len(sysArgv) < 2:
        print("Usage: python Init-New-Brain.py <New-Ecosystem-Name>")
        sysExit(1)
    init_brain(sysArgv[1])
