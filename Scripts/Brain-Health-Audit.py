#!/usr/bin/env python
# coding:utf-8
"""
ESSENTIAL PROCESS:
Audits the Obsidian vault for structural integrity, YAML compliance, and link health.

DATA FLOW:
1. Scans all .md files in the vault.
2. Parses frontmatter and extracts internal [[Links]].
3. Identifies orphans (files with no incoming links) and broken links.
4. Generates a "Coherence Report".

KEY PARAMETERS:
- VAULT_ROOT: The target directory for auditing.
- IGNORE_DIRS: Folders to skip during the scan.
"""

from sys import argv as sysArgv, exit as sysExit, stdout as sysStdout, path as sysPath
from os import walk as osWalk
from pathlib import Path
from typing import List, Set, Dict

# Add the lib directory to sys.path to import sovereignty
script_dir = Path(__file__).resolve().parent
lib_path = script_dir.parents[1] / "20-Scripts" / "lib"
sysPath.append(str(lib_path))

try:
    from sovereignty import Sovereignty
except ImportError:
    print(f"❌ Error: Could not find sovereignty.py in {lib_path}")
    sysExit(1)

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
        if (parent / "obsidian-brain").is_dir() and (parent / "fleet-operation-brain").is_dir():
            return parent
    return Path(__file__).resolve().parents[3]

WORKSPACE_ROOT = _find_workspace_root()
VAULT_ROOT = WORKSPACE_ROOT / "obsidian-brain"

IGNORE_DIRS = {
    ".git", ".obsidian", ".gemini", ".claude", ".codex", ".mistral", ".deepseek",
    "experiments", "deployments", "plans", "Templates", "99-Humans", "quick-overview"
}

# -----------------------------------------------------------------------------------------------

class BrainSentinel:
    Name = "BrainSentinel"

    def __init__(self, root: Path) -> None:
        self.root = root
        self.files: List[Path] = []
        self.valid_stems: Set[str] = set()
        self.valid_paths: Set[str] = set()
        taxonomy_path = root / "07-Core-KMS" / "tag_taxonomy.md"
        self.engine = Sovereignty(taxonomy_path)

    # -----------------------------------------------------------------------------------------------

    def scan(self) -> None:
        """
        Discovers all files and builds the relationship graph.
        """
        for root, dirs, files in osWalk(self.root):
            dirs[:] = [d for d in dirs if not d.startswith(".") and d not in IGNORE_DIRS]
            for file in files:
                path = Path(root) / file
                rel_path = path.relative_to(self.root).as_posix()
                
                if file.endswith(".md"):
                    self.files.append(path)
                    self.valid_stems.add(path.stem)
                
                self.valid_paths.add(rel_path)
                self.valid_paths.add(file) # Allow linking by filename only

    # -----------------------------------------------------------------------------------------------

    def audit(self) -> None:
        """
        Runs the validation rules using the Sovereignty engine.
        """
        for file_path in self.files:
            self.engine.audit_file(file_path, self.valid_stems, self.valid_paths)

    # -----------------------------------------------------------------------------------------------

    def auto_fix(self) -> None:
        """
        Runs the auto-fix logic using the Sovereignty engine.
        """
        for file_path in self.files:
            self.engine.auto_fix_file(file_path)

    # -----------------------------------------------------------------------------------------------

    def report(self) -> None:
        """
        Outputs the audit summary to the terminal.
        """
        report = self.engine.get_report()
        errors = report["errors"]
        warnings = report["warnings"]

        print("\n" + "="*60)
        print("🧠 BASTIEN BRAIN SENTINEL: HEALTH REPORT")
        print("="*60)
        
        print(f"\n📊 STATISTICS:")
        print(f"  - Total Markdown Files: {len(self.files)}")
        print(f"  - Total Errors: {len(errors)}")
        print(f"  - Total Warnings: {len(warnings)}")

        if errors:
            print(f"\n🚨 CRITICAL VIOLATIONS ({len(errors)}):")
            for err in errors[:15]:
                print(f"  [!] {err}")
            if len(errors) > 15:
                print(f"  ... and {len(errors) - 15} more.")

        if warnings:
            print(f"\n⚠️ HYGIENE WARNINGS ({len(warnings)}):")
            for warn in warnings[:10]:
                print(f"  [~] {warn}")
            if len(warnings) > 10:
                print(f"  ... and {len(warnings) - 10} more.")
            
        print("\n" + "="*60)
        print("📈 SYNTHESIS VERDICT:")
        
        if report["success"]:
            print("  - Accuracy:     High (0 Errors)")
            print("✨ OVERALL RESULT: BRAIN IS IN PERFECT COHERENCE")
        else:
            print(f"  - Accuracy:     Low ({len(errors)} Errors)")
            print("⚠️ OVERALL RESULT: DRIFT DETECTED. PLEASE RESOLVE THE ABOVE ISSUES.")
        print("="*60 + "\n")

# -----------------------------------------------------------------------------------------------

if __name__ == "__main__":
    sentinel = BrainSentinel(VAULT_ROOT)
    sentinel.scan()
    sentinel.auto_fix()
    sentinel.audit()
    sentinel.report()
