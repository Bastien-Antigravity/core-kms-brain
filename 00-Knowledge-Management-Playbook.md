--- 
title: "5-Dimensional Knowledge Management Playbook"
type: architecture
status: active
microservice: ecosystem-wide
tags:
  - knowledge-management
  - playbook
  - methodology
---

# 📐 5-Dimensional Knowledge Management Playbook

This document defines how to maintain and evolve the **Bastien-Antigravity** knowledge base. Mastery of these 5 dimensions ensures that information remains accessible, algorithmic, and conceptually linked.

---

## 🏗️ Dimension 1: The Physical (PARA)
Keep folders shallow. Folders represent **Physical Departments**, not categorical trees.

- **The Root Rule**: Only Master MOCs, Playbooks, and READMEs live at the root.
- **Micro-Categorization**: Documentation for a microservice lives in that microservice's actual folder (`log-server/README.md`).
- **Standard Folders**:
    - `Role-Prompts/`: The portable, generic AI agents, workflows, and dispatcher.
    - `01-Project-Business/`: Domain Driven Design, User Stories, and Epics.
    - `02-Project-Architecture/`: Core standards and ADRs specific to this project.
    - `03-Project-Coding/`: Standard idioms and toolboxes.
    - `04-Project-Deployment/`: Infrastructure and CI/CD rules.
    - `05-Project-Scripts/`: Auxiliary 20-Scripts.

---

## 🏷️ Dimension 2: The Dimensional (Tags)
Tags are cross-cutting. They allow you to filter information regardless of their physical folder.

- **Standard Nested Tags**:
    - `#type/architecture`: Fundamental system rules.
    - `#type/task`: Actionable items (picked up by dashboards).
    - `#domain/networking`: For networking-focused nodes.
    - `#state/active`: Currently relevant information.
    - `#ai/task`: Signals to the AI that this file is a direct instruction.

---

## 📊 Dimension 3: The Algorithmic (YAML & Dataview)
Every major file MUST have a YAML frontmatter block. This turns your notes into a **queryable database**.

### Standard Frontmatter
```yaml
---
microservice: <name>
type: <repository|architecture|task|session-state>
status: <active|deprecated|draft>
language: <go|rust|python|polyglot>
---
```

### Useful Dataview Queries (Copy/Paste)
**To list all tasks:**
```dataview
table status, priority from "" where type = "task" and status = "active"
```

**To list architecture by domain:**
```dataview
table microservice from "" where type = "architecture" sort file.name asc
```

---

## 🎨 Dimension 4: The Visual (Canvas)
Use `.canvas` files to map complex relationships that text cannot convey.

- **Ecosystem Topology**: Use `Ecosystem-Topology.canvas` to wire up microservice networking.
- **Event Flows**: Create canvases for transverse data paths (e.g., Ingestion -> Log-Server -> Notif-Server).
- **Rule**: If a concept involves more than 3 microservices, it deserves a Canvas map.

---

## ⚗️ Dimension 5: The Conceptual (Zettelkasten Linking)
Use bidirectional links `[[ ]]` to create an organic conceptual web.

- **The Beacon Rule**: When asking the AI for a task, link to the relevant architecture (e.g., *"Follow [[01-Facade-Pattern]]"*).
- **Atomicity**: If a file grows beyond 200 lines, **Atomize** it into smaller nodes and link them via an MOC or parent link.
- **Never Use Absolute Paths**: Always use `[[File Name]]` to ensure the graph stays healthy even if files move.

---

> [!TIP] The Workflow of Expansion
> To add a new architecture rule:
> 1. Create a file using `[[Template-Architecture]]`.
> 2. Fill in the YAML.
> 3. Link it in the **[[00-Master-MOC]]**.
