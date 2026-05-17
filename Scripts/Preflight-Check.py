#!/usr/bin/env python
# coding:utf-8
"""
ESSENTIAL PROCESS:
Cross-platform Preflight Check that runs before every squad startup.
Detects and auto-repairs common drift issues across the brain ecosystem.

DATA FLOW:
1. Resolves the workspace root from the script location.
2. Checks submodule initialization status in obsidian-brain.
3. Validates mode consistency between AI-Session-State and MODE-MANUAL.
4. Warns about non-portable paths in inventory.json.
5. Returns a status report (GREEN / YELLOW / RED).

KEY PARAMETERS:
- WORKSPACE_ROOT: Automatically detected from the script's location.
- VAULT_DIR: The obsidian-brain directory.
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


from sys import stdout as sysStdout, executable as sysExecutable
from os import name as osName
from os.path import exists as osPathExists, isdir as osPathIsdir, join as osPathJoin
from subprocess import run as subprocessRun, DEVNULL
from pathlib import Path
from re import search as reSearch
from typing import List, Tuple

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
    Works whether the script lives in core-kms-brain/Scripts/ (standalone)
    or obsidian-brain/07-Core-KMS/Scripts/ (submodule).
    """
    current = Path(__file__).resolve().parent
    for parent in [current] + list(current.parents):
        if (parent / "Bastien-Antigravity.code-workspace").exists():
            return parent
        # Root is where obsidian-brain and docker-deployment coexist
        if (parent / "obsidian-brain").is_dir() and (parent / "docker-deployment").is_dir():
            return parent
            
    # Fallback: if we are inside obsidian-brain, the root is above it
    for parent in [current] + list(current.parents):
        if parent.name == "obsidian-brain":
            return parent.parent
            
    return Path(__file__).resolve().parents[2]

WORKSPACE_ROOT = _find_workspace_root()
VAULT_DIR = WORKSPACE_ROOT / "obsidian-brain"

# Submodule mapping: folder name inside vault -> sibling repo name
SUBMODULE_MAP = {
    "01-Strategic-Nexus": "nexus-strategic-brain",
    "02-Business-BDD": "business-bdd-brain",
    "03-Tech-Stack": "tech-stack-brain",
    "04-Rapid-Prototyping": "rapid-prototyping-brain",
    "05-Fleet-Operation": "fleet-operation-brain",
    "07-Core-KMS": "core-kms-brain",
}

# -----------------------------------------------------------------------------------------------

def _check_submodules() -> Tuple[str, List[str]]:
    """
    Checks if obsidian-brain submodules are initialized.
    Auto-repairs by running 'git submodule update --init' if needed.
    Returns: (status, list_of_messages)
    """
    messages = []
    
    if not VAULT_DIR.exists():
        return "RED", ["obsidian-brain directory not found at {0}".format(VAULT_DIR)]
    
    gitmodules_path = VAULT_DIR / ".gitmodules"
    if not gitmodules_path.exists():
        return "GREEN", ["No .gitmodules found — skipping submodule check."]
    
    empty_submodules = []
    for folder_name, repo_name in SUBMODULE_MAP.items():
        submodule_path = VAULT_DIR / folder_name
        if submodule_path.exists() and osPathIsdir(str(submodule_path)):
            # Check if directory is empty (no files beyond .git)
            contents = list(submodule_path.iterdir())
            if len(contents) == 0:
                empty_submodules.append(folder_name)
            elif len(contents) == 1 and contents[0].name == ".git":
                empty_submodules.append(folder_name)
        elif not submodule_path.exists():
            empty_submodules.append(folder_name)
    
    if not empty_submodules:
        messages.append("All {0} submodules are initialized.".format(len(SUBMODULE_MAP)))
        return "GREEN", messages
    
    # Auto-repair: run git submodule update --init --recursive
    messages.append("{0} empty submodule(s) detected: {1}".format(
        len(empty_submodules), ", ".join(empty_submodules)))
    messages.append("Auto-repairing: running 'git submodule update --init --recursive'...")
    
    try:
        result = subprocessRun(
            ["git", "-C", str(VAULT_DIR), "submodule", "update", "--init", "--recursive"],
            capture_output=True, text=True, timeout=120
        )
        if result.returncode == 0:
            messages.append("Submodules initialized successfully.")
            return "YELLOW", messages
        else:
            messages.append("Submodule init failed: {0}".format(result.stderr.strip()))
            messages.append("TIP: You may need to run 'git -C obsidian-brain submodule sync' first if repo URLs changed.")
            return "RED", messages
    except Exception as e:
        messages.append("Submodule init error: {0}".format(e))
        return "RED", messages

# -----------------------------------------------------------------------------------------------

def _check_mode_consistency() -> Tuple[str, List[str]]:
    """
    Validates that AI-Session-State.md and MODE-MANUAL.md agree on the active mode.
    """
    messages = []
    
    session_state_path = VAULT_DIR / "00-AI-Orchestration" / "AI-Session-State.md"
    mode_manual_path = VAULT_DIR / "00-AI-Orchestration" / "MODE-MANUAL.md"
    
    if not session_state_path.exists() or not mode_manual_path.exists():
        messages.append("Mode files not found — skipping consistency check.")
        return "YELLOW", messages
    
    # Read MODE-MANUAL active_mode
    manual_mode = None
    with open(mode_manual_path, "r", encoding="utf-8") as f:
        for line in f:
            match = reSearch(r"active_mode:\s*(\d+)", line)
            if match:
                manual_mode = match.group(1)
                break
    
    # Read AI-Session-State active-protocol
    session_mode = None
    with open(session_state_path, "r", encoding="utf-8") as f:
        for line in f:
            match = reSearch(r"active-protocol:\s*.*Mode[- ]?(\d+)", line)
            if match:
                session_mode = match.group(1)
                break
    
    if manual_mode is None:
        messages.append("Could not read active_mode from MODE-MANUAL.md")
        return "YELLOW", messages
    
    if session_mode is None:
        messages.append("Could not read active-protocol from AI-Session-State.md")
        return "YELLOW", messages
    
    if manual_mode == session_mode:
        messages.append("Mode consistent: Mode {0} in both files.".format(manual_mode))
        return "GREEN", messages
    else:
        messages.append("MODE MISMATCH: MODE-MANUAL says Mode {0}, Session-State says Mode {1}.".format(
            manual_mode, session_mode))
        messages.append("The AI-Session-State should be updated to match.")
        return "YELLOW", messages

# -----------------------------------------------------------------------------------------------

def _check_inventory_portability() -> Tuple[str, List[str]]:
    """
    Checks that inventory.json uses portable (relative) paths.
    """
    messages = []
    
    # Updated path to match submodule structure
    inventory_path = VAULT_DIR / "05-Fleet-Operation" / "00-Repo-Control" / "inventory.json"
    if not inventory_path.exists():
        messages.append("inventory.json not found — skipping portability check.")
        return "YELLOW", messages
    
    import json
    with open(inventory_path, "r", encoding="utf-8") as f:
        try:
            inventory = json.load(f)
        except Exception:
            messages.append("inventory.json is malformed.")
            return "RED", messages
    
    absolute_paths = []
    for repo in inventory.get("repositories", []):
        path = repo.get("path", "")
        if Path(path).is_absolute():
            absolute_paths.append(repo.get("name", "unknown"))
    
    if absolute_paths:
        messages.append("{0} repo(s) use absolute paths (not portable): {1}".format(
            len(absolute_paths), ", ".join(absolute_paths[:5])))
        messages.append("TIP: Run 'python fleet-manager.py discover' to regenerate with relative paths.")
        return "YELLOW", messages
    
    messages.append("All {0} inventory paths are portable (relative).".format(
        len(inventory.get("repositories", []))))
    return "GREEN", messages

# -----------------------------------------------------------------------------------------------

def _check_essential_files() -> Tuple[str, List[str]]:
    """
    Verifies that critical ecosystem files exist.
    """
    messages = []
    essential = [
        ("AI-Init.md", VAULT_DIR / "00-AI-Orchestration" / "AI-Init.md"),
        ("AI-Session-State.md", VAULT_DIR / "00-AI-Orchestration" / "AI-Session-State.md"),
        ("MODE-MANUAL.md", VAULT_DIR / "00-AI-Orchestration" / "MODE-MANUAL.md"),
        ("Ecosystem-Map-MOC.md", VAULT_DIR / "Ecosystem-Map-MOC.md"),
        ("inventory.json", VAULT_DIR / "05-Fleet-Operation" / "00-Repo-Control" / "inventory.json"),
    ]
    
    missing = []
    for name, path in essential:
        if not path.exists():
            missing.append(name)
    
    if missing:
        messages.append("Missing essential files: {0}".format(", ".join(missing)))
        messages.append("Attempted vault path: {0}".format(VAULT_DIR))
        return "RED", messages
    
    messages.append("All {0} essential files present.".format(len(essential)))
    return "GREEN", messages

# ### MAIN ###

def run_preflight(quiet: bool = False) -> bool:
    """
    Runs all preflight checks and prints a status report.
    Returns True if all checks passed (GREEN), False otherwise.
    """
    checks = [
        ("Essential Files", _check_essential_files),
        ("Submodule Status", _check_submodules),
        ("Mode Consistency", _check_mode_consistency),
        ("Inventory Portability", _check_inventory_portability),
    ]
    
    overall = "GREEN"
    results = []
    
    for check_name, check_fn in checks:
        status, messages = check_fn()
        results.append((check_name, status, messages))
        if status == "RED":
            overall = "RED"
        elif status == "YELLOW" and overall != "RED":
            overall = "YELLOW"
    
    # Print report
    if not quiet:
        status_icons = {"GREEN": "✅", "YELLOW": "⚠️", "RED": "❌"}
        
        print("\n" + "=" * 60)
        print("🛫 PREFLIGHT CHECK REPORT")
        print("=" * 60)
        
        for check_name, status, messages in results:
            icon = status_icons.get(status, "?")
            print("\n{0} {1}: {2}".format(icon, check_name, status))
            for msg in messages:
                print("    {0}".format(msg))
        
        print("\n" + "=" * 60)
        icon = status_icons.get(overall, "?")
        if overall == "GREEN":
            print("{0} PREFLIGHT: ALL CLEAR. Ready to launch.".format(icon))
        elif overall == "YELLOW":
            print("{0} PREFLIGHT: WARNINGS DETECTED. Review above.".format(icon))
        else:
            print("{0} PREFLIGHT: CRITICAL ISSUES. Fix before proceeding.".format(icon))
        print("=" * 60 + "\n")
    
    return overall == "GREEN"

# -----------------------------------------------------------------------------------------------

if __name__ == "__main__":
    run_preflight(quiet=False)
