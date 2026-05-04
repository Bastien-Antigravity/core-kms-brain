# 🧠 Core KMS Brain (Stateless AI Engine)

Welcome to the **Core KMS Brain**. This repository is Tier 1 of the 3-Tier Knowledge Management Architecture. 

This repository is a **100% Stateless AI Engine**. It acts as the global, portable "Operating System" that drives your AI agents across any Obsidian project.

## 🏗️ Architecture & Behavior

This engine uses a Multi-Agent pipeline (Orchestrator → Architect → Developer → QA → DevOps → DocMaintainer) to autonomously write code, design metadata, and enforce standards based on an Idea Pitch.

**Why is it Stateless?**
This repository does *not* contain your project ideas, your specific variables, or your active tasks. 
It only contains the logic:
- `Role-Prompts/`: The pure instructions for the AI agents.
- `Workflows/`: The markdown rules defining how the agents interact with each other and with Git.

## 🔗 How it connects to your Project

You do not work inside this repository directly. Instead, this repository is designed to be injected as a **Git Submodule** into a wrapper `obsidian-brain` repository.

When your Gemini CLI Subagents run (initialized via `20-Scripts/start_squad.py`), they use an MCP Server to dynamically read the parent wrapper directory to find the `Project-Variables.md` and the active `10-State-and-Tasks/Inbox/`. 
This guarantees that you can globally update the AI Prompts on GitHub, pull them to any of your projects, and never experience a Git merge conflict!

For detailed instructions on how to use the Engine, please read the **[[User-Manual.md]]**.
