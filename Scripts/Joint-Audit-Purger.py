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

import os
import re
import json
import yaml
from pathlib import Path
from datetime import datetime

# Sync with RAG Engine's GLOBAL_EXCLUDES
GLOBAL_EXCLUDES = {
    '.git', '.obsidian', 'Templates', '.gemini', '.github', '.venv',
    'node_modules', 'build', 'dist', 'target', 'bin', 'out', 'venv',
    '__pycache__', '99-Humans', 'quick-overview', 'tests', '20-Scripts',
    '.claude', '.codex', '.deepseek', '.gemini'
}

def _find_vault_root():
    """Finds the obsidian-brain directory relative to the script."""
    current = Path(__file__).resolve().parent
    for parent in [current] + list(current.parents):
        vault = parent / "obsidian-brain"
        if vault.is_dir():
            return vault
    return None

def is_ignored_by_firewall(path: Path, root_dir: Path) -> bool:
    """Checks if a path is ignored by context firewalls (.aiignore etc) or carries the #ai/ignore tag."""
    try:
        current = path.resolve()
        root = root_dir.resolve()
        check_dir = current if current.is_dir() else current.parent
        while True:
            for ignore_name in [".aiignore", ".geminiignore", ".mcpignore"]:
                if (check_dir / ignore_name).exists():
                    return True
            if check_dir == root or check_dir.parent == check_dir:
                break
            check_dir = check_dir.parent
    except Exception:
        pass

    try:
        if path.is_file() and path.suffix == ".md":
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                head = f.read(1000)
                if '#ai/ignore' in head:
                    return True
    except Exception:
        pass
    return False

def joint_audit():
    root = _find_vault_root()
    if not root:
        print("Error: Could not find 'obsidian-brain' directory.")
        return

    all_md_files = []
    for r, d, fs in os.walk(root):
        # Prune excluded directories in-place
        d[:] = [dirname for dirname in d if dirname not in GLOBAL_EXCLUDES]
        
        # In-place directory ignore pruning
        current_dir = Path(r)
        is_dir_ignored = False
        for ignore_name in [".aiignore", ".geminiignore", ".mcpignore"]:
            if (current_dir / ignore_name).exists():
                is_dir_ignored = True
                break
        if is_dir_ignored:
            d[:] = []
            continue
            
        for f in fs:
            if f.endswith('.md'):
                file_path = current_dir / f
                if not is_ignored_by_firewall(file_path, root):
                    all_md_files.append(file_path)

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

    potential_deletions = []
    protected_count = 0
    
    for f in all_md_files:
        stem = f.stem
        rel_path = f.relative_to(root)
        
        try:
            with open(f, 'r', encoding='utf-8', errors='ignore') as fh:
                header = fh.read(1000)
        except:
            header = ""

        # Protect MOCs, specifications, strategic nexus notes, and core components
        is_protected = (
            stem.endswith('-MOC') or
            stem == 'README' or
            'AI-Init' in stem or
            'Session-State' in stem or
            '#type/moc' in header or
            '#type/architecture' in header or
            '#state/frozen' in header or
            '10-State-and-Tasks' in str(rel_path) or
            'Role-Prompts' in str(rel_path) or
            '02-Business-BDD' in str(rel_path) or
            '01-Strategic-Nexus' in str(rel_path) or
            'ADRs' in str(rel_path) or
            '00-AI-Orchestration' in str(rel_path) or
            '06-Microservices' in str(rel_path)
        )
        
        if stem not in linked_stems and not is_protected:
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
    
    candidates_json_path = root / "00-AI-Orchestration" / "PURGE-CANDIDATES.json"
    try:
        os.makedirs(candidates_json_path.parent, exist_ok=True)
        # Only write files if candidates are found, otherwise cleanup old ones
        if potential_deletions:
            with open(candidates_json_path, "w", encoding="utf-8") as jf:
                json.dump(potential_deletions, jf, indent=2)
            print(f"[*] Saved candidates checklist to: {candidates_json_path}")
        else:
            if candidates_json_path.exists(): os.remove(candidates_json_path)
            approval_md_path = root / "00-AI-Orchestration" / "PURGE-APPROVAL-REQUEST.md"
            if approval_md_path.exists(): os.remove(approval_md_path)
            print("\n✨ NO DARK MATTER FOUND. VAULT IS HIGHLY COHERENT.")
    except Exception as e:
        print(f"Error saving candidates JSON: {e}")
        
    if potential_deletions:
        print("\n--- CANDIDATES FOR DELETION ---")
        for p in sorted(potential_deletions):
            print(f"[!] {p}")
    print(f"============================================================")

def generate_purge_approval_request():
    root = _find_vault_root()
    if not root:
        print("Error: Could not find 'obsidian-brain' directory.")
        return

    candidates_json_path = root / "00-AI-Orchestration" / "PURGE-CANDIDATES.json"
    if not candidates_json_path.exists():
        print(f"Error: Candidates file {candidates_json_path} does not exist. Run joint_audit first.")
        return

    try:
        with open(candidates_json_path, "r", encoding="utf-8") as jf:
            candidates = json.load(jf)
    except Exception as e:
        print(f"Error reading candidates JSON: {e}")
        return

    target_md_path = root / "00-AI-Orchestration" / "PURGE-APPROVAL-REQUEST.md"
    
    lines = []
    lines.append("---")
    lines.append("microservice: obsidian-brain")
    lines.append("type: orchestration")
    lines.append("status: active")
    lines.append(f"last-updated: {datetime.now().strftime('%Y-%m-%d')}")
    lines.append("tags:")
    lines.append("- '#service/obsidian-brain'")
    lines.append("- '#type/orchestration'")
    lines.append("- '#state/active'")
    lines.append("- '#zone/3-fleet'")
    lines.append("---")
    lines.append("# 🧹 Dark Matter Purging Review Checklist")
    lines.append("")
    lines.append("> [!IMPORTANT]")
    lines.append("> The following files are identified as 'Dark Matter' (orphan files with no incoming links).")
    lines.append("> Review the candidates below and toggle the checkbox to `[x] Keep` or `[x] Delete` to authorize action.")
    lines.append("")
    lines.append("## 📦 Scan Summary")
    lines.append(f"- **Scan Date**: {datetime.now().strftime('%Y-%m-%d')}")
    lines.append(f"- **Total Candidates Found**: {len(candidates)}")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    if not candidates:
        lines.append("### ✨ No candidates found. Vault is highly coherent!")
    else:
        for idx, rel_path in enumerate(sorted(candidates)):
            full_path = root / rel_path
            title = rel_path
            summary = "No description available."
            tags = []
            
            if full_path.exists():
                try:
                    with open(full_path, "r", encoding="utf-8", errors="ignore") as fh:
                        content = fh.read()
                        
                    title_match = re.search(r"^#\s+(.*)$", content, re.MULTILINE)
                    if title_match:
                        title = title_match.group(1).strip()
                        
                    body_text = content
                    if content.startswith("---"):
                        fm_parts = content.split("---", 2)
                        if len(fm_parts) >= 3:
                            body_text = fm_parts[2]
                            try:
                                fm = yaml.safe_load(fm_parts[1])
                                if isinstance(fm, dict):
                                    tags = fm.get("tags", [])
                            except:
                                pass
                                
                    clean_body = re.sub(r"[#*`>_\-\[\]]", " ", body_text).strip()
                    clean_body = re.sub(r"\s+", " ", clean_body)
                    if clean_body:
                        summary = clean_body[:180] + "..." if len(clean_body) > 180 else clean_body
                except Exception as e:
                    summary = f"Error reading candidate: {e}"
            
            lines.append(f"### {idx+1}. `{rel_path}`")
            lines.append(f"- **Document Title**: *{title}*")
            if tags:
                tag_str = ", ".join([f"`{t}`" for t in tags])
                lines.append(f"- **Tags**: {tag_str}")
            lines.append(f"- **Preview**: {summary}")
            lines.append("- **Verification**: No other Obsidian note links to this file.")
            lines.append("- **Review Action**:")
            lines.append("  - [ ] **Keep** (Retain file as is)")
            lines.append("  - [ ] **Delete** (Remove file permanently)")
            lines.append("")
            lines.append("---")
            lines.append("")
            
    try:
        os.makedirs(target_md_path.parent, exist_ok=True)
        with open(target_md_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print(f"[*] Generated Approval Request Checklist at: {target_md_path}")
    except Exception as e:
        print(f"Error generating approval request: {e}")

def execute_purge():
    """Reads the approval checklist and deletes files marked for deletion."""
    root = _find_vault_root()
    if not root:
        print("Error: Could not find 'obsidian-brain' directory.")
        return

    approval_md_path = root / "00-AI-Orchestration" / "PURGE-APPROVAL-REQUEST.md"
    if not approval_md_path.exists():
        print(f"Error: Approval checklist {approval_md_path} does not exist.")
        return

    try:
        with open(approval_md_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading approval checklist: {e}")
        return

    purge_blocks = re.findall(r"### \d+\. `([^`]+)`.*?\[\s*\]\s+\*\*Keep\*\*.*?\[[xX]\]\s+\*\*Delete\*\*", content, re.DOTALL)
    
    if not purge_blocks:
        print("No files marked for deletion in the checklist.")
        return

    print(f"🚀 Found {len(purge_blocks)} files authorized for deletion.")
    deleted_count = 0
    for rel_path in purge_blocks:
        full_path = root / rel_path
        if full_path.exists():
            try:
                os.remove(full_path)
                print(f"  [X] Deleted: {rel_path}")
                deleted_count += 1
            except Exception as e:
                print(f"  [!] Failed to delete {rel_path}: {e}")
        else:
            print(f"  [?] File already gone: {rel_path}")

    print(f"\n✨ Purge complete. {deleted_count} files removed.")
    
    candidates_json_path = root / "00-AI-Orchestration" / "PURGE-CANDIDATES.json"
    try:
        if approval_md_path.exists(): os.remove(approval_md_path)
        if candidates_json_path.exists(): os.remove(candidates_json_path)
        print("[*] Cleanup: Removed checklist and candidates files.")
    except Exception as e:
        print(f"Error during cleanup: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--ai-classify":
            print("Starting AI-Assisted classification phase...")
            generate_purge_approval_request()
        elif sys.argv[1] == "--execute":
            print("Starting Purge Execution phase...")
            execute_purge()
        elif sys.argv[1] == "--help" or sys.argv[1] == "-h":
            print("Usage: python Joint-Audit-Purger.py [OPTION]")
            print("Options:")
            print("  (none)         Run scan and generate PURGE-CANDIDATES.json")
            print("  --ai-classify  Generate PURGE-APPROVAL-REQUEST.md from candidates")
            print("  --execute      Delete files marked with [x] Delete in the checklist")
        else:
            print(f"Unknown option: {sys.argv[1]}")
            sys.exit(1)
    else:
        joint_audit()
