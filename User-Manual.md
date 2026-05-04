# 📖 Core KMS Brain: User Manual

Welcome to the AI Engine User Manual. This document explains how the Multi-Agent Engine functions and how you can interact with it across any of your projects.

## 1. Core Principles of the Engine
The engine is driven by a sequential pipeline:
1. **Idea Pitch**: You write a raw idea.
2. **Orchestrator**: Breaks the idea into a Master Plan.
3. **Architect**: Designs the technical blueprint or metadata schema.
4. **Developer**: Writes the code or templates.
5. **QA**: Validates behavior using BDD specifications.
6. **DevOps**: Generates CI/CD or deployment 20-Scripts.
7. **DocMaintainer**: Wires the final output into the Obsidian Knowledge Graph and preserves session history.

## 2. Engaging the AI Engine
There are three ways to interact with the AI Squad, depending on your goal:

### Tier 1: Direct AI Interaction
Best for general queries and brainstorming.
- **How**: Launch the orchestrator via `./20-Scripts/start_squad.py` and chat directly.

### Tier 2: Operational Modes (Protocols)
Best for enforcing strict engineering rules (e.g., Spec-First).
- **How**: Switch the `active_mode` in **[[00-AI-Orchestration/MODE-MANUAL]]**. The AI will automatically adapt its behavior based on the current protocol.

### Tier 3: Squad Delegation (Custom Prompts)
Best for expert tasks (QA review, BDD drafting).
- **How**: Delegate directly to a subagent persona. 
- **Examples**:
   - *"Ask the Orchestrator to break this idea into a Master Plan."*
   - *"Ask QA to validate the BDD specs."*

---

## 3. Initializing a Session (MANDATORY)
To ensure the squad remembers its context across different repositories:
1. **Initialize**: At the start of every session, tell the AI: *"Read AI-Init.md and AI-Session-State.md."*
2. **Commit State**: Before closing the session, ask the AI to update the local `AI-Session-State.md` with its progress.

## 4. Modifying the Engine
If you find that an AI Agent is consistently making a mistake, you should update its Prompt!
1. Open the specific prompt in `07-Core-KMS/Role-Prompts/`.
2. Add your new behavioral rule.
3. Update the Gemini subagent by running `./20-Scripts/convert_agents.py`.
4. Commit and push the changes.

## 5. Initializing a New Project
If you have created an empty `obsidian-brain` project and cloned this Core as a submodule, simply copy the `.gemini` folder and `20-Scripts/` directory to instantly empower the new project with your AI Squad!
