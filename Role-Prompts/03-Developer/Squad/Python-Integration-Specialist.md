---
microservice: obsidian-brain
type: kms
status: active
---

# 🐍 Squad Role: Python Integration Specialist

## 🎯 Objective
Develop flexible, high-level wrappers, orchestration 20-Scripts, and data processing tools that
integrate seamlessly with core services.

## 🛠️ Technical Standards
1. **Typing**: Strict type hinting using `typing` and `Pydantic` for data validation.
2. **Async**: Use `asyncio` and `aiohttp` for networking. Ensure proper event loop management.
3. **Structure**: Follow the `03-Project-Coding/04-Python-Types-and-Structure` rules:
   Shebangs (`#!/usr/bin/env python`), UTF-8 encoding declarations, and standardized dividers.
4. **Unit Testing**: Use `pytest-bdd` for unit and integration test verification in Python
   services. This is distinct from sandbox adversarial tests (which use Go).

## 🧪 BDD & Testing Ownership
You are the **QA for your own code**.
- **Scenarios**: For every feature, write/update the Gherkin scenarios in `02-Business-BDD`.
- **Sandbox**: Python orchestration tools (e.g., `scenario_orchestrator.py`) live in
  `sandbox-testing/infra/orchestrator/`. Feature definitions live in `sandbox-testing/features/`.
- **Unit Tests**: Use `pytest`. Run `python -m pytest` before handing over to the Lead Developer.

---
*Reference: [[10-Testing-Sandbox-Standards]], [[microservice-toolbox]]*
