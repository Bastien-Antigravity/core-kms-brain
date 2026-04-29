---
type: architecture-blueprint
status: draft
role: architect
---
# Architecture Blueprint: [Feature/Bug Name]

## 1. Context Injection
> **Mandatory Check**: I have verified this design against `01-Project-Architecture/Global-Architecture-Rules.md`.

## 2. Research Findings
*Summary of how the current codebase handles this area (e.g., "Currently, config-server uses a hardcoded map for X").*

## 3. Proposed Interfaces & Models
*Define the Go interfaces, Rust traits, or Python protocols here. Do NOT write business logic.*
```go
// Example
type IFeature interface {
    DoThing() error
}
```

## 4. Ecosystem Impact
*Does this change require NATS event changes? Safe-socket protocol changes? If yes, list them.*

## 5. Next Step
Pass this document to the **Developer**.
