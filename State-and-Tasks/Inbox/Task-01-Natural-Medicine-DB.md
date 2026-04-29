---
type: task-plan
status: pending
role: architect
---
# Master Plan: Natural Medicine Knowledge Graph

## 1. Goal Overview
The user wants to create a highly structured Obsidian database for Natural Medicine. The goal is to cross-reference illnesses/health problems with natural products (and grandmother's remedies) using reliable sources. 
The system must be fully searchable bidirectionally (Illness -> Product, Product -> Illness) and account for double-effects or negative interactions.

## 2. Context & Constraints
- **Environment**: This is an Obsidian-native project. The "code" we are writing consists of Markdown Templates and Dataview algorithms, rather than traditional Go/Rust microservices.
- **Bidirectional Links**: We must heavily utilize Dataview YAML frontmatter to establish the relationships between entities.
- **Scalability**: The definition and metadata schema must be evolvable.

## 3. Hand-off Tasks

### 🛠️ Architect Tasks
- [ ] Design the Metadata Schema (YAML frontmatter) for two distinct entities: `Type: Illness` and `Type: Product`.
- [ ] Define the relational arrays required (e.g., `treats: []`, `side_effects: []`, `interactions: []`, `sources: []`).
- [ ] Output `Template-02-Architecture-Blueprint.md` detailing the YAML schema design.

### 🧪 QA Tasks (BDD Spec Enforcer)
- [ ] Read the Architect's Blueprint.
- [ ] Write a `Template-03-QA-Test-Spec.md` that defines the expected behavior (e.g., "Given a Product note with `treats: [Headache]`, When I open the Headache note, Then the Dataview table should display that product").

### 💻 Developer Tasks
- [ ] Implement the actual Obsidian Templates (`Template-Illness.md` and `Template-Product.md`) based on the Architect's schema.
- [ ] Write the Dataview query algorithms inside those templates to automatically generate the bidirectional tables.

### 🚀 DevOps Tasks
- [ ] Not applicable for an Obsidian-native database. (Skip)

### 📚 DocMaintainer Tasks
- [ ] Link the new Database templates into the `00-Master-MOC.md`.
- [ ] Update the Project Business folder with the new functional scope.
- [ ] Append task summary to `AI-Session-State.md`.

## 4. Next Step
The Dispatcher will now route this task to the **Architect**.
