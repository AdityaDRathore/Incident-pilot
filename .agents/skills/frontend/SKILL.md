---
name: frontend
description: Build the engineering dashboard against stable API/event contracts.
---

# IncidentPilot Frontend

## Description
Build the engineering dashboard against stable API/event contracts.

## Steps

1. Verify API/event contracts.
2. Delegate to `incidentpilot-frontend`.
3. Build:
   - dashboard
   - incident list
   - incident detail
   - timeline
   - evidence
   - hypotheses
   - agent trace
   - remediation
   - approval
   - audit log
   - report
   - evaluation dashboard
4. Connect SSE/WebSocket events.
5. Add demo scenario launcher.
6. Test loading/error/empty/disconnected states.
7. Run frontend build, lint, and type checks.
8. Perform browser verification where supported.

## Exit Criteria

A new user can launch a seeded incident and observe investigation through resolution in the UI.
