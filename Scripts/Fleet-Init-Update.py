#!/usr/bin/env python
# coding:utf-8

import json
from pathlib import Path

# -----------------------------------------------------------------------------------------------

# Configurations
INVENTORY_PATH = Path("/Users/imac/Desktop/Bastien-Antigravity/obsidian-brain/fleet-operation-brain/00-Repo-Control/inventory.json")

TEMPLATE = """# ⚡ AI Initialization: {repo_name}

> [!IMPORTANT] MANDATORY INITIALIZATION
> Copy and paste this prompt when starting a new session in this repository:
> 
> "1. Read the ecosystem map in **[[Ecosystem-Map-MOC]]**."
> "2. Load project constraints from **[[AI-Project-DNA]]**."
> "3. Restore session state from **[[AI-Session-State]]**."
> "4. **Sentinel Audit**: Run `python3 core-kms-brain/Scripts/Brain-Health-Audit.py` and resolve any drift."
> "5. **Squad Protocol**: You are now the **Lead Developer**. Identify and hire the required **Specialists** from `core-kms-brain/Role-Prompts/03-Developer/Squad/`."
"""

# -----------------------------------------------------------------------------------------------

def update_fleet():
    if not INVENTORY_PATH.exists():
        print(f"Error: Inventory not found at {INVENTORY_PATH}")
        return

    with open(INVENTORY_PATH, 'r') as f:
        data = json.load(f)

    repos = data.get("repositories", [])
    print(f"🚀 Starting Fleet-Wide AI-Init Update for {len(repos)} repositories...")

    for repo in repos:
        name = repo.get("name")
        path = Path(repo.get("path"))
        
        if not path.exists():
            print(f"  [!] Skipping {name}: Path does not exist ({path})")
            continue

        init_file = path / "AI-Init.md"
        content = TEMPLATE.format(repo_name=name)
        
        try:
            with open(init_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  [+] Updated: {name}")
        except Exception as e:
            print(f"  [X] Failed {name}: {str(e)}")

    print("\n✅ Fleet Update Complete.")

# -----------------------------------------------------------------------------------------------

if __name__ == "__main__":
    update_fleet()
