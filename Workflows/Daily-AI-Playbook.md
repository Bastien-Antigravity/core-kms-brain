---
title: "Daily AI Playbook"
type: architecture
status: active
microservice: ecosystem-wide
tags:
  - ai/workflow
  - ai/playbook
---

# 📐 Daily AI Playbook

This document defines the standardized operational loop for working with the Antigravity AI assistant.

## 1. Starting the Session (The Ritual)
Always restore context and **Audit** the environment to prevent drift.
1. **Restore State**: Read [[AI-Session-State]] and [[AI-Project-DNA]].
2. **Audit Environment**: Run `git branch --show-current` and check `VERSION.txt`. Verify they match the session state.
3. **Spec Specialist Rule**: If starting a new feature, you MUST transition to the **Spec Specialist** role and draft a BDD spec in `business-bdd-brain/02-Behavior-Specs/`.

2. **Spec Phase**: Draft/Update a `.md` file in `business-bdd-brain/02-Behavior-Specs/[repo-name]/`.
3. **Purger Gate (The "Straight-to-Goal" Check)**: 
    - **Principle**: Activate the **Purger** role to review the implementation plan. 
    - **Challenge**: For every new feature proposed, the AI MUST search for and identify at least one opportunity to **Consolidate** or **Simplify** existing patterns that the new feature overlaps with.
    - **Goal**: Ensure the net complexity of the microservice remains as low as possible.
    - **Approval**: AI must not implement until the file header contains `status: approved` and the "Simplification Review" is documented.

## 2. AI Handover Protocol (State Machine)
To prevent context loss and AI drift when switching roles, you MUST use the Inbox files as a state machine.
- When finishing your task as one role, DO NOT rely on conversational memory for the next role.
- Open the relevant task file in `state-and-tasks/Inbox/`.
- Update the YAML frontmatter: change `status: active` to `status: pending` and set `role: <next_role>`.
- The `Agent-Dispatcher.py` script will parse this frontmatter to seamlessly hand over the context.

---

## ⚡ Quick-Start Magic Prompt
Copy and paste this at the start of any new session to perfectly orient the AI:

> *"1. Read the ecosystem map in **[[00-Master-MOC]]**."*
> *"2. Load project constraints from **[[AI-Project-DNA]]**."*
> *"3. Restore session state from **[[AI-Session-State]]**."*
> *"4. **Audit**: Run `git branch --show-current` and check `VERSION.txt` to verify environment matches state."*
> *"5. **Spec Gate**: Before implementing any feature, act as a **Spec Specialist** to draft/find a Gherkin spec in `business-bdd-brain/02-Behavior-Specs/` and obtain my approval."*

## 3. The Development Loop (Execution)
When I am coding, I must follow these mandatory steps:
- **Build First**: Run `python tech-stack-brain/05-Project-Scripts/Build-Wrapper.py` to validate code locally.
- **Commit Often**: Use Conventional Commits (`feat:`, `fix:`, `refactor:`).
- **Branch Strategy**: Follow the `develop` -> `main` flow defined in [[Git-Branching-Rules]].
    - *Pro-Tip*: Always commit to `develop` first, then merge to `main` to keep your production branch clean and protected.

## 4. Closing the Session (Evening)
Save the progress so we can resume seamlessly tomorrow.
1. **Purger Phase (Garbage Collection)**: Before closing, you MUST assume the **Purger** role (`08-Purger/Mister-Straight-to-Goal.md`). Delete any temporary files, redundant yaml configurations, and obsolete scratchpads.
2. **Command**: *"Save session state"*
3. **Reference**: Update [[AI-Session-State]] with accurate progress.

## 5. The Integrity Loop (Autonomous Doc Cleanup)
When a task is complete, the AI must automatically:
1. **Sync READMEs**: Update any microservice `README.md` impacted by code changes.
2. **Update Session-State**: Log the latest local progress in the repo-specific `AI-Session-State.md`.
3. **Bridge to Brain**: Update the `00-Master-MOC` or any Architecture node if a new system-wide rule is discovered.

## 6. The Wisdom Feedback Loop (Maintenance)
To keep the "Experience Ledger" alive, we use a post-session ritual:
1. **Extraction**: At the end of every significant task, the AI asks: *"Did we learn a universal lesson today?"*
2. **Recording**: If yes, the AI updates the relevant log in `tech-stack-brain/06-Role-Wisdom/`.
3. **Pruning**: Once a month, the AI performs a "Knowledge Compression" to remove redundant or outdated wisdom.

---

## ⚡ Quick-Start Magic Prompt
Copy and paste this at the start of any new session to perfectly orient the AI:

> *"Restore session state from **[[00-AI-Engine/state-and-tasks/AI-Session-State]]** and read the ecosystem map in **[[00-Master-MOC]]**. Follow the standardized loop in **[[Daily-AI-Playbook]]**."*

---
> [!TIP] Use the Beacons!
> You can point me to any architectural rule by using the `[[ ]]` link syntax in the chat box or in your task files!
