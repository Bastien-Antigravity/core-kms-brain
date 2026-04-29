import os
import glob
import sys

def init_brain(ecosystem_name):
    print(f"Initializing new AI Brain for: {ecosystem_name}")
    
    core_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    wrapper_dir = os.path.dirname(core_dir)
    
    project_vars_path = os.path.join(wrapper_dir, "Project-Variables.md")
    inbox_dir = os.path.join(wrapper_dir, "State-and-Tasks", "Inbox")
    session_state_path = os.path.join(wrapper_dir, "State-and-Tasks", "AI-Session-State.md")
    
    # 1. Update Project Variables
    try:
        with open(project_vars_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        with open(project_vars_path, 'w', encoding='utf-8') as f:
            for line in lines:
                if line.startswith('ecosystem_name:'):
                    f.write(f'ecosystem_name: "{ecosystem_name}"\n')
                else:
                    f.write(line)
        print("[-] Updated Project-Variables.md")
    except Exception as e:
        print(f"[!] Error updating Project-Variables: {e}")

    # 2. Clear Inbox (except Templates)
    try:
        for file in glob.glob(os.path.join(inbox_dir, "*.md")):
            os.remove(file)
            print(f"[-] Deleted old task: {os.path.basename(file)}")
    except Exception as e:
        print(f"[!] Error clearing Inbox: {e}")

    # 3. Clear Session State
    try:
        with open(session_state_path, 'w', encoding='utf-8') as f:
            f.write("# Central AI Session State\n\n*Brain Initialized. Ready for tasks.*")
        print("[-] Cleared AI-Session-State.md")
    except Exception as e:
        print(f"[!] Error clearing Session State: {e}")
        
    print("\n[SUCCESS] Brain successfully initialized! You can now write your Idea Pitch.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python Init-New-Brain.py <New-Ecosystem-Name>")
        sys.exit(1)
    init_brain(sys.argv[1])
