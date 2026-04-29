---
type: qa-test-spec
status: draft
role: qa
---
# BDD Test Specification: [Feature/Bug Name]

## 1. Context Injection
> **Mandatory Check**: I have read the `Master-Plan.md` and the `Architecture-Blueprint.md` to perfectly align these expectations with the Orchestrator's original idea.

## 2. Gherkin Scenarios
*Write strict BDD specifications that the codebase MUST pass inside the `sandbox-testing` microservice.*

### Scenario 1: [Name]
- **Given** [Initial State / Ecosystem Context]
- **When** [Action / Event Trigger]
- **Then** [Expected Output / State Change]

### Scenario 2: [Name]
- **Given** ...
- **When** ...
- **Then** ...

## 3. Sandbox Testing Implementation
*If applicable, write the initial skeleton for the test file to be placed in the sandbox-testing repo.*

```python
# sandbox-testing/tests/test_feature.py
def test_scenario_1():
    # Given
    pass
    # When
    pass
    # Then
    pass
```

## 4. Next Step
Pass this Test Specification to the **Developer**. The Developer MUST write code that makes these specific tests pass.
