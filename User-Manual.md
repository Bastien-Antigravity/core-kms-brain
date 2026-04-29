# 📖 AI Engine: User Manual

Welcome to the AI Engine. This generic framework turns any language model (via `gemini-cli`) into an autonomous team of software engineers.

## 1. Quick Start: Your First Idea
To kick off the pipeline, you need to provide the Orchestrator with an Idea Pitch.
1. Navigate to `00-AI-Engine/State-and-Tasks/Inbox/Templates/`.
2. Copy `Template-00-Idea-Pitch.md` and save it to `Inbox/Idea-MyNewFeature.md`.
3. Fill out the sections: Feature Name, Expected Behavior (BDD), and Target Microservices.
4. Let the automated Dispatcher take over (or run `gemini-cli` manually with the Orchestrator prompt).

## 2. Secrets & Tokens Management
The Engine requires access to secrets (like GitHub tokens) to push code or trigger CI/CD pipelines.
**CRITICAL RULE**: Never store secrets in Markdown files within this vault.
Instead, the DevOps and Developer agents are programmed to strictly read from your **System Environment Variables**.

**How to set this up:**
Before running the `Agent-Dispatcher.py` or manually running `gemini-cli`, ensure your terminal has the necessary environment variables exported:
- **Windows (PowerShell)**: `$env:GITHUB_TOKEN="your_token_here"`
- **Linux/Mac (Bash)**: `export GITHUB_TOKEN="your_token_here"`

The AI will generate scripts (e.g., `deploy.sh`) that use `$GITHUB_TOKEN` to authenticate dynamically.

## 3. Repo State Persistence (History)
While the central `00-AI-Engine` manages active tasks in its `Inbox/`, it is critical to preserve the historical context of what happens *within* each microservice.
- Every microservice repository has its own local `AI-Session-State.md` file (e.g., `../config-server/AI-Session-State.md`).
- At the end of every pipeline loop, the **DocMaintainer Agent** automatically appends a summary of the completed task to the specific microservice's local state file.
- This ensures that if you switch from `config-server` to `safe-socket` and back, the Engine retains the full historical context of that specific repository!

## 4. The Autonomous Dispatcher
The `Agent-Dispatcher.py` script is the beating heart of the Engine.
It reads the `Inbox/` directory, checks the `role` and `status` of each file, and automatically executes `gemini-cli` with the correct Role Prompt.
- **Run Manually**: `python 00-AI-Engine/Scripts/Agent-Dispatcher.py`
- **Run Automatically**: Attach the script to a CRON job or Windows Task Scheduler to run every hour.

## 4. Portability: Moving to a New Project
This Engine is entirely decoupled from your specific code. If you want to use it on a new project:
1. Copy the entire `00-AI-Engine/` folder to the new project's Obsidian Vault.
2. Open `Context-Interface/Project-Variables.md`.
3. Update the `ecosystem_name` and the paths pointing to your local Architecture and Coding rules.
4. The Engine will instantly adapt to the new ruleset.
