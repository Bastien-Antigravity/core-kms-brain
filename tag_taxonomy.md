---
microservice: core-kms-brain
type: governance
status: active
tags:
- '#service/core-kms-brain'
- '#type/governance'
- '#state/active'
- '#zone/3-fleet'
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
- **#type/governance**: AI session initialization, audit scripts, and ritual prompts (e.g., `AI-Init.md`).
- **#type/fleet-op**: Global fleet operational READMEs, registries, and strategies.
- **#type/fleet-action-plan**: Migration, refactoring, and update checklists (e.g., FAP series).
- **#type/deployment-log**: Post-deployment audit logs and trace logs.
- **#type/service-hub**: Operational hub files mapping specific microservice details (specs, code, dashboards).
- **#type/protocol**: Technical protocols defining standardized conventions and behavior in the fleet.
- **#type/dashboard**: Interactive monitoring web application or system status UI.

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

## 4. #service/ (Microservice Identity)
- **#service/<name>**: Direct linkage to a specific repository or microservice (e.g., `#service/safe-socket`).

## 5. #tech/ (Technology Stack)
- **#tech/<name>**: Language, framework, or infrastructure tool (e.g., `#tech/go`, `#tech/docker`).

## 6. #tier/ (Architectural Topology)
- **#tier/1-gateway**: Edge layer services.
- **#tier/2-logic**: Business logic and analysis.
- **#tier/3-core**: Central aggregation.
- **#tier/4-infra**: Base infrastructure.

## 7. #zone/ (Governance Level)
- **#zone/1-frozen**: Immutable behavioral specs.
- **#zone/2-fluid**: Rapid prototypes and experiments.
- **#zone/3-fleet**: Global CI/CD and ops.

## 8. #ai/ (AI Processing Rules)
- **#ai/ignore**: Flag for human-centric documentation that should be ignored by AI context gathering.

## 9. #role/ (Persona & Operator Responsibilities)
- **#role/human-onboarding**: Guides for humans onboarding to a role.
- **#role/<name>**: Direct linkage to a specific AI squad role or persona (e.g. `#role/developer`).

---
> [!IMPORTANT]
> The **Sentinel** (`Brain-Health-Audit.py`) enforces that every file contains at least one `#type/` and one `#state/` tag.
