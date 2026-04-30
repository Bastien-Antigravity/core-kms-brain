# 📖 Core KMS Brain: User Manual

Welcome to the AI Engine User Manual. This document explains how the Multi-Agent Engine functions and how you can interact with it across any of your projects.

## 1. Core Principles of the Engine
The engine is driven by a sequential pipeline:
1. **Idea Pitch**: You write a raw idea.
2. **Orchestrator**: Breaks the idea into a Master Plan.
3. **Architect**: Designs the technical blueprint or metadata schema.
4. **Developer**: Writes the code or templates.
5. **QA**: Validates behavior using BDD specifications.
6. **DevOps**: Generates CI/CD or deployment scripts.
7. **DocMaintainer**: Wires the final output into the Obsidian Knowledge Graph and preserves session history.

## 2. Using the Engine in a Project
Because this `core-kms-brain` is a Git Submodule, you will not write your Idea Pitches inside this repository! 

**To launch a task:**
1. Navigate to the root of your wrapper `obsidian-brain` repository.
2. Open `state-and-tasks/Inbox/`.
3. Create a new markdown file using the `Template-00-Idea-Pitch.md`.
4. Run the Python dispatcher:
   ```bash
   python core-kms-brain/Scripts/Agent-Dispatcher.py
   ```
5. The dispatcher will dynamically detect your active project variables and begin routing the task through the agents.

## 3. Modifying the Engine
If you find that an AI Agent is consistently making a mistake, you should update its Prompt!
1. Open the specific prompt in `core-kms-brain/Role-Prompts/`.
2. Add your new behavioral rule (e.g., "Always use `snake_case` for Dataview fields").
3. Commit and push the change to the `core-kms-brain` GitHub repository.
4. Go to your other projects and run `git submodule update --remote` to instantly upgrade their AI Engine!

## 4. Initializing a New Project
If you have created an empty `obsidian-brain` project and cloned this Core as a submodule, you can automatically set up the wrapper environment by running:
```bash
python core-kms-brain/Scripts/Init-New-Brain.py "My-New-Project-Name"
```
This script will instantly generate the empty `Inbox/`, `Project-Variables.md`, and `AI-Session-State.md` at the root of your project, completely ready for your first Idea Pitch!
