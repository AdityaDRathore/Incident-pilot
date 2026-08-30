---
name: integrate
description: Connect the independently built layers into one working application.
---

# IncidentPilot Integration

## Description
Connect the independently built layers into one working application.

## Steps

1. Verify backend API.
2. Verify simulator APIs.
3. Verify agent tools.
4. Connect agent tools to simulator.
5. Connect persistence/checkpointing.
6. Connect RAG retrieval to investigation.
7. Run:
   - DB pool scenario
   - bad deployment scenario
   - Redis scenario
8. Verify evidence IDs propagate from tools to conclusions.
9. Verify hypothesis status transitions.
10. Verify remediation planning.
11. Verify policy checks.
12. Verify human approval pause.
13. Approve a simulated remediation.
14. Verify resume occurs from persisted state.
15. Verify recovery telemetry changes.
16. Verify report generation.
17. Run tests and fix defects.

## Exit Criteria

At least three scenarios complete end-to-end without bypassing policy or state persistence.
