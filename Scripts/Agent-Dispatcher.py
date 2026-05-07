#!/usr/bin/env python
# coding:utf-8
"""
ESSENTIAL PROCESS:
Monitors the 'Inbox' directory in the Obsidian Vault for pending tasks
and automates the handover to specific AI Agent personas.

DATA FLOW:
1. Scans obsidian-brain/10-State-and-Tasks/Inbox for markdown files.
2. Parses YAML frontmatter to identify tasks with 'status: pending'.
3. Updates the status to 'active' for tasks assigned to known roles.
4. (Simulation) Triggers the appropriate AI persona workflow.

KEY PARAMETERS:
- ROLE_MAP: Dictionary mapping agent roles to their prompt files.
- INBOX_DIR: Target directory for incoming task definitions.
"""

from os.path import dirname as osPathDirname, abspath as osPathAbspath, join as osPathJoin, exists as osPathExists
from glob import glob as globGlob
from typing import Optional, Dict, Any

# ### CONFIGURATIONS ###

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

WORKSPACE_ROOT = _find_workspace_root()

# Path to the obsidian vault
OBSIDIAN_DIR = osPathJoin(WORKSPACE_ROOT, "obsidian-brain")
INBOX_DIR = osPathJoin(OBSIDIAN_DIR, "10-State-and-Tasks", "Inbox")
ROLE_PROMPTS_DIR = osPathJoin(WORKSPACE_ROOT, "core-kms-brain", "Role-Prompts")

# Role to Prompt Mapping
ROLE_MAP = {
    "oracle": "00-Oracle/Prompt-Chronos-Oracle.md",
    "orchestrator": "01-Orchestrator/Prompt-Orchestrator.md",
    "architect": "02-Architect/Prompt-Architect.md",
    "developer": "03-Developer/Prompt-Lead-Developer.md",
    "qa": "04-QA/Prompt-QA.md",
    "fleetarchitect": "05-FleetArchitect/Prompt-Fleet-Architect.md",
    "docmaintainer": "06-DocMaintainer/Prompt-DocMaintainer.md",
    "fleetcommander": "07-FleetCommander/Prompt-FleetCommander.md",
    "purger": "08-Purger/Mister-Straight-to-Goal.md",
    "sentinel": "09-Sentinel/Prompt-Sentinel.md",
}

# -----------------------------------------------------------------------------------------------

def parse_frontmatter(file_path: str) -> Optional[Dict[str, Any]]:
    """
    Parses YAML frontmatter from a markdown file using a late import.
    """
    # Late import for specialized library
    from yaml import safe_load as yamlSafeLoad

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            try:
                frontmatter = yamlSafeLoad(parts[1])
                return frontmatter
            except Exception as e:
                print(f"AgentDispatcher: Error parsing YAML in {file_path}: {e}")
    return None

# -----------------------------------------------------------------------------------------------

def process_inbox() -> None:
    """
    Iterates through the inbox and transitions tasks from pending to active.
    """
    if not osPathExists(INBOX_DIR):
        print(f"AgentDispatcher: Inbox directory not found at {INBOX_DIR}")
        return

    task_files = globGlob(osPathJoin(INBOX_DIR, "*.md"))
    
    for task_file in task_files:
        if "Template" in task_file:
            continue # Skip templates
            
        frontmatter = parse_frontmatter(task_file)
        if not frontmatter:
            continue
            
        status = frontmatter.get('status')
        role = frontmatter.get('role')
        
        if status == 'pending' and role in ROLE_MAP:
            print(f"[*] Simulating handover for {task_file} (Role: {role})")
            
            # Simulated handover: read file, replace 'status: pending' with 'status: active'
            try:
                with open(task_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                new_content = content.replace('status: pending', 'status: active', 1)
                
                with open(task_file, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print("    Handover complete. Status updated to 'active'.")
            except Exception as e:
                print(f"    Error updating status: {e}")
        elif status == 'completed':
            print(f"[-] Skipping completed task: {task_file}")

# -----------------------------------------------------------------------------------------------

if __name__ == "__main__":
    print("Starting Agent Dispatcher...")
    process_inbox()
    print("Run complete.")
