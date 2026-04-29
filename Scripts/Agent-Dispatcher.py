import os
import glob
import subprocess
import yaml

# Configurations
INBOX_DIR = "../State-and-Tasks/Inbox/"
ROLE_PROMPTS_DIR = "../Role-Prompts/"

# Role to Prompt Mapping
ROLE_MAP = {
    "orchestrator": "01-Orchestrator/Prompt-Orchestrator.md",
    "architect": "02-Architect/Prompt-Architect.md",
    "developer": "03-Developer/Prompt-Developer.md",
    "qa": "04-QA/Prompt-QA.md",
    "devops": "05-DevOps/Prompt-DevOps.md",
    "docmaintainer": "06-DocMaintainer/Prompt-DocMaintainer.md"
}

def parse_frontmatter(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            try:
                frontmatter = yaml.safe_load(parts[1])
                return frontmatter
            except Exception as e:
                print(f"Error parsing YAML in {file_path}: {e}")
    return None

def process_inbox():
    task_files = glob.glob(os.path.join(INBOX_DIR, "*.md"))
    
    for task_file in task_files:
        if "Template" in task_file:
            continue # Skip templates
            
        frontmatter = parse_frontmatter(task_file)
        if not frontmatter:
            continue
            
        status = frontmatter.get('status')
        role = frontmatter.get('role')
        
        if status == 'pending' and role in ROLE_MAP:
            print(f"[*] Processing {task_file} for role: {role}")
            
            prompt_file = os.path.join(ROLE_PROMPTS_DIR, ROLE_MAP[role])
            
            # Construct gemini-cli command
            cmd = [
                "gemini-cli",
                "--system-prompt-file", prompt_file,
                "--file", task_file
            ]
            
            print(f"    Running: {' '.join(cmd)}")
            
            try:
                # Execute the CLI (Uncomment to actually run)
                # result = subprocess.run(cmd, capture_output=True, text=True, check=True)
                # print(f"    Success! Output captured.")
                # TODO: Parse output, append to files, and update frontmatter to next role.
                pass
            except subprocess.CalledProcessError as e:
                print(f"    Error running CLI: {e.stderr}")
        elif status == 'completed':
            print(f"[-] Skipping completed task: {task_file}")

if __name__ == "__main__":
    print("Starting Agent Dispatcher...")
    process_inbox()
    print("Run complete.")
