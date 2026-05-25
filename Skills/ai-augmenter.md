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
# AI Augmenter Skill

Instructs agents on how to run LLM-based pre-processing and context enrichment on raw text/code chunks.

## 🧠 Cognitive Enrichment Protocol

1. **Hypothetical Questions (RAG Query Enrichment)**:
   - For every text chunk, generate 3 potential high-quality questions a developer or user might ask that are directly answered by this chunk.
   - Example: For a RAG server initialization chunk, questions like: "How is the Chroma client initialized?", "What settings are used for telemetry?".

2. **Summarization (Child-to-Parent Reference)**:
   - Generate a single-sentence summary of the main action or fact in the chunk.
   - This summary acts as a high-density reference key.

3. **Multi-Vector Routing**:
   - Save the raw chunk as the **Parent Document** (heavy text, contains code or long explanations).
   - Embed and index the **Child Summaries** and **Questions** (short, highly semantic, rapid matching).
   - Map child vectors to parent IDs in ChromaDB for automated resolving upon query.
