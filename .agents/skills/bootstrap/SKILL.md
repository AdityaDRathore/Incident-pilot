---
name: bootstrap
description: Establish architecture and contracts before parallel implementation.
---

# IncidentPilot Bootstrap

## Description
Establish architecture and contracts before parallel implementation.

## Steps

1. Act as `incidentpilot-lead`.
2. Inspect the repository and all existing source/configuration.
3. Read the IncidentPilot master specification available in the workspace.
4. Read `.agents/rules/incidentpilot.md`.
5. Determine what already exists; never assume a blank repository.
6. Design the target architecture.
7. Create:
   - `docs/architecture.md`
   - `docs/decisions.md`
   - `docs/build-plan.md`
8. Create `/contracts` and define:
   - agent state
   - tool contracts
   - API contracts
   - database contracts
   - event contracts
   - evaluation contracts
   - security contracts
9. Define ownership boundaries for the nine custom agents.
10. Run architecture sanity checks.
11. Do not begin broad feature implementation.
12. End with a concise status report and recommended next workflow.

## Exit Criteria

Architecture and contracts exist, are internally consistent, and are sufficient for independent implementation agents to proceed.
