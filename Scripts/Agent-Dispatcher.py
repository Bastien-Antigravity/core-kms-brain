#!/usr/bin/env python
# coding:utf-8
"""
ESSENTIAL PROCESS:
Monitors the Obsidian Vault recursively for pending tasks
and automates the handover to specific AI Agent personas.

DATA FLOW:
1. Scans the entire obsidian-brain recursively for markdown files.
2. Parses YAML frontmatter to identify tasks with 'status: pending'.
3. Updates the status to 'active' for tasks assigned to known roles.
4. (Simulation) Triggers the appropriate AI persona workflow.

KEY PARAMETERS:
- ROLE_MAP: Dictionary mapping agent roles to their prompt files.
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

def process_vault_tasks() -> None:
    """
    Scans the entire vault for files with '#state/pending' tag and handles handover.
    """
    from glob import glob as globGlob
    
    # 1. Discover all markdown files in the vault (Discovery-Based)
    all_files = globGlob(osPathJoin(OBSIDIAN_DIR, "**", "*.md"), recursive=True)
    print(f"[*] Scanning {len(all_files)} files for pending tasks...")
    
    for task_file in all_files:
        if ".git" in task_file or ".obsidian" in task_file:
            continue
            
        # Optimization: Quick string check before heavy YAML parsing
        try:
            with open(task_file, 'r', encoding='utf-8') as f:
                head = f.read(1000) # Read enough to catch YAML
        except:
            continue
            
        if "#state/pending" in head:
            frontmatter = parse_frontmatter(task_file)
            if not frontmatter:
                continue
            
            role = frontmatter.get('role')
            # Check if role is in our map or if it's explicitly tagged as a task
            if role in ROLE_MAP:
                print(f"[!] Pending task found: {task_file} (Role: {role})")
                
                # Update status in content
                try:
                    with open(task_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Transition both the legacy field and the new tag
                    new_content = content.replace('status: pending', 'status: active')
                    new_content = new_content.replace('#state/pending', '#state/active')
                    
                    with open(task_file, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"    Handover complete. Transitioned to #state/active.")
                except Exception as e:
                    print(f"    Error updating task: {e}")

# -----------------------------------------------------------------------------------------------

if __name__ == "__main__":
    print("Starting Agent Dispatcher (Tag-Driven Mode)...")
    process_vault_tasks()
    print("Run complete.")
