---
ecosystem_name: "Test-AI-Engine"
architecture_rules_path: "tech-stack-brain/02-Project-Architecture/Global-Architecture-Rules.md"
coding_standards_path: "tech-stack-brain/03-Project-Coding/00-Coding-Style-Guide.md"
master_moc_path: "00-Master-MOC.md"
---

# Project Context Map

This file links the agnostic `00-AI-Engine` to the specific project it is currently embedded in.

When an AI Agent is instantiated, it MUST read the YAML frontmatter of this file to understand:
1. The `ecosystem_name` it is working on.
2. The paths to the critical rule documents.
