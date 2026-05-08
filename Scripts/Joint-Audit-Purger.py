import os
import re
from pathlib import Path

def _find_vault_root():
    """Finds the obsidian-brain directory relative to the script."""
    current = Path(__file__).resolve().parent
    for parent in [current] + list(current.parents):
        vault = parent / "obsidian-brain"
        if vault.is_dir():
            return vault
    return None

def joint_audit():
    root = _find_vault_root()
    if not root:
        print("Error: Could not find 'obsidian-brain' directory.")
        return

    ignore_dirs = {'.git', '.obsidian', 'Templates'}
    
    all_md_files = []
    for r, d, fs in os.walk(root):
        if any(x in r for x in ignore_dirs):
            continue
        for f in fs:
            if f.endswith('.md'):
                all_md_files.append(Path(r) / f)

    all_stems = {f.stem for f in all_md_files}
    linked_stems = set()
    
    for f in all_md_files:
        try:
            with open(f, 'r', encoding='utf-8', errors='ignore') as fh:
                content = fh.read()
                # Match Obsidian [[links]]
                links = re.findall(r'\[\[([^|\]]+)(?:\|[^\]]*)?\]\]', content)
                for l in links:
                    linked_stems.add(Path(l).stem)
        except Exception:
            continue

    # Sentinel + Purger Joint Filtering
    potential_deletions = []
    protected_count = 0
    
    for f in all_md_files:
        stem = f.stem
        rel_path = f.relative_to(root)
        
        try:
            with open(f, 'r', encoding='utf-8', errors='ignore') as fh:
                header = fh.read(1000) # Read enough for YAML
        except:
            header = ""

        # 🛡️ SENTINEL PROTECTION RULES (Why we KEEP an orphan)
        # Added Tag-Awareness: Protect #type/moc, #type/architecture, #state/frozen
        is_protected = (
            stem.endswith('-MOC') or
            stem == 'README' or
            'AI-Init' in stem or
            'Session-State' in stem or
            '#type/moc' in header or
            '#type/architecture' in header or
            '#state/frozen' in header or
            '.gemini' in str(rel_path) or
            '10-State-and-Tasks' in str(rel_path) or
            'Role-Prompts' in str(rel_path) or
            '02-Business-BDD' in str(rel_path) or
            '01-Strategic-Nexus' in str(rel_path) or
            'ADRs' in str(rel_path) or
            '06-Microservices' in str(rel_path)
        )
        
        if stem not in linked_stems and not is_protected:
            # 🧹 PURGER CLASSIFICATION (Why we might DELETE)
            potential_deletions.append(str(rel_path))
        elif stem not in linked_stems and is_protected:
            protected_count += 1

    print(f"============================================================")
    print(f"🧹 PURGER AUDIT: DARK MATTER SCAN")
    print(f"============================================================")
    print(f"Total MD Files Scanned: {len(all_md_files)}")
    print(f"Protected Orphans (Kept): {protected_count}")
    print(f"Potential Dark Matter (For Deletion): {len(potential_deletions)}")
    print(f"------------------------------------------------------------")
    
    if potential_deletions:
        print("\n--- CANDIDATES FOR DELETION ---")
        for p in sorted(potential_deletions):
            print(f"[!] {p}")
    else:
        print("\n✨ NO DARK MATTER FOUND. VAULT IS HIGHLY COHERENT.")
    print(f"============================================================")

if __name__ == "__main__":
    joint_audit()
