# 🤖 The AI Engine ("Core-Brain")

Welcome to the fully portable, autonomous AI Engine. This folder contains the underlying logic, roles, and automation scripts that turn any LLM (via `gemini-cli`) into a specialized "Team of Agents".

## 1. Portability (How to embed this Engine)
This Engine is strictly decoupled from the project it operates on. To drop this Engine into a new project:
1. Copy this `00-AI-Engine` folder into your new Obsidian vault.
2. Open `Context-Interface/Project-Variables.md`.
3. Update the `ecosystem_name` and the paths to your local architecture rules and MOCs.
All Agent Prompts will automatically read these variables and adapt to the new project.

## 2. The Roles
The Engine splits complex work into specialized roles, located in `Role-Prompts/`:
1. **Orchestrator**: Researches the codebase and splits Ideas into specific `Task.md` files.
2. **Architect**: Designs the system interfaces and checks them against Global Rules.
3. **QA**: Uses Behavior-Driven Development (BDD) to write `Test-Spec.md` expectations.
4. **Developer**: Writes the actual code to make the QA specs pass.
5. **DevOps**: Handles CI/CD, Docker, and environment configuration.
6. **DocMaintainer**: Organizes the Knowledge Graph, tags, and closes the loop.

## 3. Automation (The Dispatcher)
You do not need to manually chat with each agent. The Engine includes an autonomous dispatcher.
1. Run `python Scripts/Agent-Dispatcher.py` (You can attach this to Windows Task Scheduler to run hourly).
2. The Dispatcher reads `State-and-Tasks/Inbox/`.
3. It maps pending tasks to the correct Agent Prompt and automatically runs `gemini-cli`.
4. The output is captured, and the task is moved down the pipeline autonomously.

## 4. Workflows
Read `Workflows/Workflow-Idea-to-Exploitation.md` to see exactly how context is handed off between agents using strict Markdown templates.
