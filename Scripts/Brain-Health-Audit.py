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

from sys import argv as sysArgv, exit as sysExit, stdout as sysStdout
from os import walk as osWalk
from re import findall as reFindall
from pathlib import Path
from typing import List, Set, Dict

# Standardize terminal output encoding for Windows
if sysStdout.encoding != 'utf-8':
    try:
        sysStdout.reconfigure(encoding='utf-8')
    except (AttributeError, Exception):
        pass

# ### CONFIGURATIONS ###

SCRIPT_DIR = Path(__file__).resolve().parent
# core-kms-brain/Scripts -> parent is core-kms-brain -> parent is root
WORKSPACE_ROOT = SCRIPT_DIR.parents[1]
VAULT_ROOT = WORKSPACE_ROOT / "obsidian-brain"

IGNORE_DIRS = {".git", ".obsidian", "state-and-tasks/Inbox/Templates"}

# Mandatory YAML fields
REQUIRED_FIELDS = ["type", "status"]

# -----------------------------------------------------------------------------------------------

class BrainSentinel:
    Name = "BrainSentinel"

    def __init__(self, root: Path) -> None:
        self.root = root
        self.files: List[Path] = []
        self.link_map: Dict[str, Set[str]] = {} # file_name -> {outgoing_links}
        self.incoming_links: Dict[str, Set[str]] = {} # file_name -> {incoming_files}
        self.errors = {
            "missing_yaml": [],
            "broken_links": [],
            "orphans": [],
            "mode_mismatch": []
        }

    # -----------------------------------------------------------------------------------------------

    def _get_clean_name(self, path: Path) -> str:
        """
        Returns the stem (filename without extension) as the canonical name.
        """
        return path.stem

    # -----------------------------------------------------------------------------------------------

    def scan(self) -> None:
        """
        Discovers all files and builds the relationship graph.
        """
        for root, dirs, files in osWalk(self.root):
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
            for file in files:
                if file.endswith(".md"):
                    path = Path(root) / file
                    self.files.append(path)
                    name = self._get_clean_name(path)
                    self.link_map[name] = self._extract_links(path)
                    
                    # Track incoming links
                    for link in self.link_map[name]:
                        if link not in self.incoming_links:
                            self.incoming_links[link] = set()
                        self.incoming_links[link].add(name)

    # -----------------------------------------------------------------------------------------------

    def _extract_links(self, path: Path) -> Set[str]:
        """
        Extracts [[Link]] patterns from file content.
        """
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Regex for [[File Name]] or [[File Name|Alias]]
        links = reFindall(r'\[\[([^|\]]+)(?:\|[^\]]*)?\]\]', content)
        return set(links)

    # -----------------------------------------------------------------------------------------------

    def audit(self) -> None:
        """
        Runs the validation rules against the scanned data.
        """
        all_names = {self._get_clean_name(f) for f in self.files}
        all_relative_paths = {f.relative_to(self.root).with_suffix('').as_posix() for f in self.files}
        
        # Discover all files on disk (including non-md) for link validation
        all_files_on_disk = set()
        for root, dirs, files in osWalk(self.root):
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
            for file in files:
                rel_path = Path(root).relative_to(self.root) / file
                # Normalize to forward slashes for cross-platform linking
                rel_path_posix = rel_path.as_posix()
                all_files_on_disk.add(rel_path_posix)
                all_files_on_disk.add(file) # Allow linking by filename only

        for file_path in self.files:
            name = self._get_clean_name(file_path)
            
            # 1. Check YAML
            self._check_yaml(file_path)
            
            # 2. Check Broken Links
            for link in self.link_map[name]:
                # Normalize link to forward slashes
                link_normalized = link.replace("\\", "/")
                
                # Check if it's a markdown file (name or rel path)
                if link_normalized in all_names or link_normalized in all_relative_paths:
                    continue
                
                # Check if it's an exact file on disk (with extension)
                if link_normalized in all_files_on_disk:
                    continue
                
                # Check if adding .md makes it valid
                if "{0}.md".format(link_normalized) in all_files_on_disk:
                    continue

                # Check if adding .canvas makes it valid
                if "{0}.canvas".format(link_normalized) in all_files_on_disk:
                    continue

                # Also check if it's a stem of a path-like link
                link_stem = Path(link_normalized).stem
                if link_stem in all_names:
                    continue

                self.errors["broken_links"].append("{0} -> [[{1}]]".format(name, link))
            
            # 3. Check Orphans
            if name not in self.incoming_links or len(self.incoming_links[name]) == 0:
                # Exclude MOCs and root READMEs from being orphans
                if not name.endswith("-MOC") and not name == "README":
                    self.errors["orphans"].append(name)

    # -----------------------------------------------------------------------------------------------

    def _check_yaml(self, path: Path) -> None:
        """
        Verifies mandatory frontmatter fields.
        """
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        name = self._get_clean_name(path)
        if not content.startswith("---"):
            self.errors["missing_yaml"].append(f"{name} (No Frontmatter)")
            return

        parts = content.split("---", 2)
        if len(parts) < 3:
            self.errors["missing_yaml"].append(f"{name} (Malformed YAML)")
            return
            
        yaml_content = parts[1]
        for field in REQUIRED_FIELDS:
            if f"{field}:" not in yaml_content:
                self.errors["missing_yaml"].append(f"{name} (Missing {field})")

    # -----------------------------------------------------------------------------------------------

    def report(self) -> None:
        """
        Outputs the audit summary to the terminal.
        """
        print("\n" + "="*60)
        print("🧠 BASTIEN BRAIN SENTINEL: HEALTH REPORT")
        print("="*60)
        
        print(f"\n📊 STATISTICS:")
        print(f"  - Total Files: {len(self.files)}")
        print(f"  - Active Connections: {sum(len(v) for v in self.link_map.values())}")

        print(f"\n🚨 YAML VIOLATIONS ({len(self.errors['missing_yaml'])}):")
        for err in self.errors["missing_yaml"][:10]:
            print(f"  [!] {err}")
        if len(self.errors["missing_yaml"]) > 10:
            print(f"  ... and {len(self.errors['missing_yaml']) - 10} more.")

        print(f"\n🔗 BROKEN LINKS ({len(self.errors['broken_links'])}):")
        for err in self.errors["broken_links"][:10]:
            print(f"  [X] {err}")

        print(f"\n👻 ORPHANED KNOWLEDGE ({len(self.errors['orphans'])}):")
        for err in self.errors["orphans"][:10]:
            print(f"  [?] {err}")
            
        print("\n" + "="*60)
        if not any(self.errors.values()):
            print("✨ RESULT: BRAIN IS IN PERFECT COHERENCE")
        else:
            print("⚠️ RESULT: DRIFT DETECTED. PLEASE RESOLVE THE ABOVE ISSUES.")
        print("="*60 + "\n")

# -----------------------------------------------------------------------------------------------

if __name__ == "__main__":
    sentinel = BrainSentinel(VAULT_ROOT)
    sentinel.scan()
    sentinel.audit()
    sentinel.report()
