---
microservice: core-kms-brain
type: guideline
status: active
tags:
- '#service/core-kms-brain'
- '#type/guideline'
- '#state/active'
- '#zone/3-fleet'
---
# AST Chunker Skill

Guides agents on how to partition codebase files into syntactically valid code blocks instead of generic text splits.

## 🛠️ Syntactic Partitioning Rules

1. **Language Detection**:
   - `.py`: Use the built-in Python `ast` module to extract classes and top-level functions.
   - `.go`, `.rs`, `.cpp`, `.js`, `.ts`: Use matching brace algorithms (`{` ... `}`) to extract function/struct blocks cleanly.

2. **Signature Extraction**:
   - Always include the full function/class signature (e.g. `func (s *Server) Start() error {`) at the start of the chunk.
   - Capture leading comments/docstrings explaining the function immediately preceding the signature.

3. **Size Optimization**:
   - If a function is extremely long, do not cut it randomly. Keep it as a single chunk, but record parent/child nested structures.
   - Ensure the line bounds (`start_line`, `end_line`) are explicitly saved in the chunk metadata.
