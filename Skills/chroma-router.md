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
# Chroma Router Skill

Outlines the collection separation, routing boundaries, and database query-resolution rules.

## 🗂️ RAG Ingestion & Routing Strategy

1. **Schema Partitioning**:
   - **Main Collection**: `obsidian_brain`. Stores both child semantic pointers (summaries/questions) and parent chunks.
   - **Exclusion Filters**: Metadata tags `is_child: True` and `is_parent: True` separate retrieval targets.

2. **Retrieval Mechanics**:
   - Queries must embed and search against `is_child: True` entries to maximize semantic match accuracy.
   - If a matching child document is found, resolve its `parent_id` from metadata.
   - Return the parent block's full text to the LLM context, ensuring the LLM receives complete, unbroken code/docs instead of fragmented summaries.
