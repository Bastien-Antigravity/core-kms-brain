---
type: architecture
status: active
tags:
- '#state/active'
- null
- '#type/architecture'
---

# 🏷️ Tag Taxonomy: Source of Truth

This document defines the controlled vocabulary for tagging files within the Bastien-Antigravity ecosystem. All automated scripts and manual notes MUST adhere to these tags to ensure system-wide interoperability.

## 1. #type/ (Content Classification)
- **#type/moc**: Map of Content / Index file.
- **#type/architecture**: High-level structural rules and diagrams.
- **#type/spec**: BDD Behavior Specifications (Given/When/Then).
- **#type/guide**: How-to documentation and tutorials.
- **#type/reference**: API definitions, schemas, or glossaries.
- **#type/task**: Actionable tasks or session logs.
- **#type/wisdom**: Lessons learned and AI experience extraction.

## 2. #state/ (Operational Status)
- **#state/active**: Currently used and valid.
- **#state/pending**: Awaiting action (e.g., Task handover).
- **#state/draft**: Incomplete or undergoing review.
- **#state/deprecated**: Obsolete but kept for historical context.
- **#state/frozen**: Permanent architectural rules (Zone 1).

## 3. #domain/ (Functional Area)
- **#domain/networking**: Safe-socket, TCP, etc.
- **#domain/logging**: Universal-logger, Flexible-logger.
- **#domain/config**: Distributed-config, Config-server.
- **#domain/fleet**: Fleet-manager, sub-repo orchestration.

---
> [!IMPORTANT]
> The **Sentinel** (`Brain-Health-Audit.py`) enforces that every file contains at least one `#type/` and one `#state/` tag.
