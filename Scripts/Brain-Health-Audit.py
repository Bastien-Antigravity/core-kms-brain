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
"""

import os
import re
from pathlib import Path
from typing import List, Set, Dict

# -----------------------------------------------------------------------------------------------

# Configurations
SCRIPT_DIR = Path(__file__).resolve().parent
VAULT_ROOT = SCRIPT_DIR.parents[1]
IGNORE_DIRS = {".git", ".obsidian", "state-and-tasks/Inbox/Templates"}

# Mandatory YAML fields
REQUIRED_FIELDS = ["type", "status"]

# -----------------------------------------------------------------------------------------------

class BrainSentinel:
    def __init__(self, root: Path):
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

    def _get_clean_name(self, path: Path) -> str:
        return path.stem

    def scan(self):
        """Discovers all files and builds the relationship graph."""
        for root, dirs, files in os.walk(self.root):
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

    def _extract_links(self, path: Path) -> Set[str]:
        """Extracts [[Link]] patterns from file content."""
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Regex for [[File Name]] or [[File Name|Alias]]
        links = re.findall(r'\[\[([^|\]]+)(?:\|[^\]]*)?\]\]', content)
        return set(links)

    def audit(self):
        """Runs the validation rules."""
        all_names = {self._get_clean_name(f) for f in self.files}
        
        for file_path in self.files:
            name = self._get_clean_name(file_path)
            
            # 1. Check YAML
            self._check_yaml(file_path)
            
            # 2. Check Broken Links
            for link in self.link_map[name]:
                if link not in all_names:
                    self.errors["broken_links"].append(f"{name} -> [[{link}]]")
            
            # 3. Check Orphans
            if name not in self.incoming_links or len(self.incoming_links[name]) == 0:
                # Exclude MOCs and root READMEs from being orphans
                if not name.endswith("-MOC") and not name == "README":
                    self.errors["orphans"].append(name)

    def _check_yaml(self, path: Path):
        """Verifies mandatory frontmatter fields."""
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

    def report(self):
        """Outputs the audit summary."""
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
