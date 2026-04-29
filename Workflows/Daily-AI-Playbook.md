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

## 1. Starting the Session (Morning)
Always restore the last known context to ensure I'm aware of the current state and pending bugs.
- **Command**: *"Restore session state"*
- **Reference**: [[AI-Session-State]]

## 2. Requesting New Features or Bug Fixes
To keep the chat clean and the logic structured, use the **Inbox** folder.
1. Create a new `.md` file in `00-AI-Engine/State-and-Tasks/Inbox/`.
2. Use the `[[Template-AI-Task]]` to fill in requirements.
3. Tag the file with `type: task` and `status: active`.
4. **Command**: *"Antigravity, please execute the task in [[Inbox/Your-New-Task]]."*

## 3. The Development Loop (Execution)
When I am coding, I must follow these mandatory steps:
- **Build First**: Run `python obsidian-brain/05-Scripts/Build-Wrapper.py` to validate code locally.
- **Commit Often**: Use Conventional Commits (`feat:`, `fix:`, `refactor:`).
- **Branch Strategy**: Follow the `develop` -> `main` flow defined in [[Git-Branching-Rules]].
    - *Pro-Tip*: Always commit to `develop` first, then merge to `main` to keep your production branch clean and protected.

## 4. Closing the Session (Evening)
Save the progress so we can resume seamlessly tomorrow.
- **Command**: *"Save session state"*
- **Reference**: [[AI-Session-State]]

## 5. The Integrity Loop (Autonomous Doc Cleanup)
When a task is complete, the AI must automatically:
1. **Sync READMEs**: Update any microservice `README.md` impacted by code changes.
2. **Update Session-State**: Log the latest local progress in the repo-specific `AI-Session-State.md`.
3. **Bridge to Brain**: Update the `00-Master-MOC` or any Architecture node if a new system-wide rule is discovered.

---

## ⚡ Quick-Start Magic Prompt
Copy and paste this at the start of any new session to perfectly orient the AI:

> *"Restore session state from **[[00-AI-Engine/State-and-Tasks/AI-Session-State]]** and read the ecosystem map in **[[00-Master-MOC]]**. Follow the standardized loop in **[[Daily-AI-Playbook]]**."*

---
> [!TIP] Use the Beacons!
> You can point me to any architectural rule by using the `[[ ]]` link syntax in the chat box or in your task files!
