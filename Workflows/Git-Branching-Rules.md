# AI Workflow & Orchestration Guidelines 🚀 `Status: Active`

This document governs how the AI assistant operates inside the `{{ECOSYSTEM_NAME}}` polyrepo ecosystem. AI agents must enforce these operational rules precisely.

## 1. Commit and Branching Rules
- **Direct Pushes strictly forbidden**: Never push directly to `main`. If you generate a deployment script (`run_command`), the branch pipeline must strictly follow:
  ```powershell
  git checkout develop
  git pull origin develop --rebase # MANDATORY: Prevent merge conflicts!
  git commit -m "<Type>(<Scope>): <Description>"
  git push origin develop
  git checkout main
  git pull origin main --rebase
  git merge develop
  git push origin main
  ```
- **Commit Formatting**: All commits **MUST** follow the Conventional Commits specification:
  - `feat`: A new feature
  - `fix`: A bug fix
  - `chore`: Maintenance, dependencies, style fixes
  - `test`: Adding missing tests
  - `refactor`: Restructuring code with no logic changes

## 2. Local Testing Constraints (MANDATORY)
- **Local Testing First**: The `antigravity-workspace/` folder currently lives locally at the root of the workspace. You MUST use these scripts to validate code changes locally **before** you even propose or execute a deployment script to GitHub.
- To validate a specific repo: Run `python obsidian-brain/05-Scripts/Build-Wrapper.py test <repo_name>`
- To validate the entire workspace: Run `python obsidian-brain/05-Scripts/Multi-Repo-Validator.py build`
- Never write a `git push` script unless the local testing orchestration cleanly reports a `[SUCCESS]`.

## 3. Automation and Dependencies
- **Dependency Bumps**: When requested to bump a core library (like `safe-socket`), the AI must update it globally across all impacted repositories if not caught by `Dependabot`.
- **Artifact Generation**: Use Markdown Artifact files natively to show major implementation plans. Emphasize "Dry-Runs" for all large architectural migrations.

## 4. Universal Scripts & Local Tooling
- Do not expect global system-tools like `curl`, `jq`, or `sed`. Rely on the `{{ECOSYSTEM_NAME}}/` tooling engine structure to orchestrate complex validation across folders.
## 5. Documentation & Brain Integrity (MANDATORY)

To ensure the ecosystem remains professional and the AI remains "Project Aware," the following autonomous rules apply:
- **Autonomous Doc Updates**: Any code change (feat, fix, refactor) that modifies public APIs, configuration parameters, or setup steps MUST be accompanied by an automatic update of the corresponding `README.md`, `ARCHITECTURE.md`, or `TESTING.md` in the same repository.
- **Brain Maintenance**: After completing a task, the AI MUST check if any Map of Content (MOC), Topology Canvas, or Zettelkasten nodes in the `obsidian-brain` require synchronization or new links.
- **Context Preservation**: Every session and significant feature completion MUST finalize with an update to the repository-specific `AI-Session-State.md`.

