#!/usr/bin/env python
# coding:utf-8

import os
import shutil
from pathlib import Path
import time

OBSIDIAN_DIR = Path(__file__).resolve().parents[2]
WORKSPACE_DIR = OBSIDIAN_DIR.parent

def purge_stale_state():
    """Rule: Stale AI-Session-State.md summaries."""
    print("[*] Checking for stale state files (older than 30 days)...")
    now = time.time()
    count = 0
    for state_file in WORKSPACE_DIR.rglob("AI-Session-State.md"):
        # Don't delete the central one in obsidian-brain
        if "obsidian-brain" in str(state_file): 
            continue
        if state_file.stat().st_mtime < now - 30 * 86400:
            os.remove(state_file)
            print(f"    Deleted stale state: {state_file}")
            count += 1
    if count == 0:
        print("    No stale state files found.")

def main():
    print("Starting Maintenance Skill (Purger Mode)...")
    purge_stale_state()
    print("Maintenance complete.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "purge":
        main()
    else:
        print("Usage: python Maintenance-Skill.py purge")
