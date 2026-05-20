#!/usr/bin/env python
# coding:utf-8
"""
ESSENTIAL PROCESS:
Propagates the standardized AI-Init.md file across all repositories 
defined in the fleet inventory.

DATA FLOW:
1. Reads the global repository list from inventory.json.
2. For each repository, generates an AI-Init.md file from a template.
3. Overwrites the existing AI-Init.md in each target repository root.

KEY PARAMETERS:
- INVENTORY_PATH: Path to the fleet registry (JSON).
- TEMPLATE: The markdown content for the initialization prompt.
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


from json import load as jsonLoad
from pathlib import Path
from sys import stdout as sysStdout

# Standardize terminal output encoding for Windows
if sysStdout.encoding != 'utf-8':
    try:
        sysStdout.reconfigure(encoding='utf-8')
    except (AttributeError, Exception):
        pass

# ### CONFIGURATIONS ###

def _find_workspace_root() -> Path:
    """
    Walk up from this script's location until we find the workspace root.
    """
    current = Path(__file__).resolve().parent
    for parent in [current] + list(current.parents):
        if list(parent.glob("*.code-workspace")):
            return parent
        if (parent / "obsidian-brain").is_dir() and (parent / "fleet-operation-brain").is_dir():
            return parent
    return Path(__file__).resolve().parents[1]

WORKSPACE_ROOT = _find_workspace_root()

# Path to the inventory (fleet-operation-brain is a sibling of core-kms-brain)
INVENTORY_PATH = WORKSPACE_ROOT / "fleet-operation-brain" / "00-Repo-Control" / "inventory.json"

TEMPLATE = """---
microservice: {repo_name}
type: governance
status: active
---

# ⚡ AI Initialization: {repo_name}

> [!IMPORTANT] MANDATORY INITIALIZATION
> Copy and paste this prompt when starting a new session in this repository:
> 
> "1. Read the ecosystem map in **[[Ecosystem-Map-MOC]]**."
> "2. Load project constraints from **[[AI-Project-DNA]]**."
> "3. Restore session state from **[[AI-Session-State]]**."
> "4. **Sentinel Audit**: Run `python core-kms-brain/Scripts/Brain-Health-Audit.py` and resolve any drift."
> "5. **Squad Protocol**: You are now the **Lead Developer**. Identify and hire the required **Specialists** from `core-kms-brain/Role-Prompts/03-Developer/Squad/`."
"""

# -----------------------------------------------------------------------------------------------

def update_fleet() -> None:
    """
    Scans the inventory and updates the AI-Init.md file for every registered repository.
    """
    if not INVENTORY_PATH.exists():
        print("FleetUpdate: Inventory not found at {0}".format(INVENTORY_PATH))
        return

    with open(INVENTORY_PATH, 'r', encoding='utf-8') as f:
        data = jsonLoad(f)

    repos = data.get("repositories", [])
    print("🚀 Starting Fleet-Wide AI-Init Update for {0} repositories...".format(len(repos)))

    for repo in repos:
        name = repo.get("name")
        path_str = repo.get("path")
        
        if not path_str:
            continue
        
        # Resolve relative paths against workspace root
        path = Path(path_str)
        if not path.is_absolute():
            path = (WORKSPACE_ROOT / path_str).resolve()
        
        if not path.exists():
            print("  [!] Skipping {0}: Path does not exist ({1})".format(name, path))
            continue

        init_file = path / "AI-Init.md"
        content = TEMPLATE.format(repo_name=name)
        
        try:
            with open(init_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print("  [+] Updated: {0}".format(name))
        except Exception as e:
            print("  [X] Failed {0}: {1}".format(name, str(e)))

    print("\n✅ Fleet Update Complete.")

# -----------------------------------------------------------------------------------------------

if __name__ == "__main__":
    update_fleet()
