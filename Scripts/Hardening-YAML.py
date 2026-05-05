import os
import re
from pathlib import Path

VAULT_ROOT = Path(__file__).resolve().parents[2]

# Mapping of folder prefixes to metadata
ZONE_MAP = {
    "00-AI-Orchestration": {"type": "governance", "status": "active"},
    "01-Strategic-Nexus": {"type": "strategy", "status": "active"},
    "02-Business-BDD": {"type": "spec", "status": "frozen"},
    "03-Tech-Stack": {"type": "architecture", "status": "active"},
    "04-Rapid-Prototyping": {"type": "experiment", "status": "fluid"},
    "05-Fleet-Operation": {"type": "fleet-op", "status": "active"},
    "06-Microservices": {"type": "hub", "status": "active"},
    "07-Core-KMS": {"type": "kms", "status": "active"},
    "10-State-and-Tasks": {"type": "task", "status": "active"},
    "20-Scripts": {"type": "automation", "status": "active"},
}

def apply_hardening(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    relative_path = file_path.relative_to(VAULT_ROOT)
    parts = relative_path.parts
    
    # Determine zone-based defaults
    zone = parts[0] if parts else ""
    defaults = ZONE_MAP.get(zone, {"type": "note", "status": "active"})
    
    # Determine microservice
    microservice = "obsidian-brain"
    if zone == "06-Microservices" and len(parts) > 1:
        # Try to extract microservice name from Hub file
        hub_match = re.search(r"([\w-]+)-Hub", parts[-1])
        if hub_match:
            microservice = hub_match.group(1).lower()

    new_frontmatter = {
        "microservice": microservice,
        "type": defaults["type"],
        "status": defaults["status"]
    }

    if content.startswith("---"):
        # Update existing frontmatter
        fm_parts = content.split("---", 2)
        if len(fm_parts) >= 3:
            fm_content = fm_parts[1]
            body = fm_parts[2]
            
            for key, val in new_frontmatter.items():
                if f"{key}:" not in fm_content:
                    fm_content = f"{key}: {val}\n" + fm_content
            
            new_content = f"--- \n{fm_content.strip()}\n---{body}"
        else:
            # Malformed, treat as no frontmatter for safety
            fm_header = "\n".join([f"{k}: {v}" for k, v in new_frontmatter.items()])
            new_content = f"---\n{fm_header}\n---\n\n{content}"
    else:
        # Create new frontmatter
        fm_header = "\n".join([f"{k}: {v}" for k, v in new_frontmatter.items()])
        new_content = f"---\n{fm_header}\n---\n\n{content}"

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

def main():
    print("[*] Starting batch YAML hardening...")
    count = 0
    for root, dirs, files in os.walk(VAULT_ROOT):
        if ".git" in root or ".obsidian" in root:
            continue
        for file in files:
            if file.endswith(".md"):
                path = Path(root) / file
                apply_hardening(path)
                count += 1
    print(f"[*] Hardened {count} files.")

if __name__ == "__main__":
    main()
