---
name: build-core
description: Build the backend, agent core, simulator, and RAG layers in parallel where their contracts permit.
---

# IncidentPilot Build Core

## Description
Build the backend, agent core, simulator, and RAG layers in parallel where their contracts permit.

## Steps

1. Verify `/contracts` exists and is coherent.
2. Delegate the following in parallel:
   - `incidentpilot-backend`
   - `incidentpilot-agent-core`
   - `incidentpilot-simulator`
   - `incidentpilot-rag`
3. Give each agent its full scoped instructions and require tests.
4. Prefer isolated Git worktrees for implementation agents when supported.
5. Monitor all agents.
6. When each completes, inspect:
   - diff
   - tests
   - contract compliance
   - dependency changes
7. Integrate completed work.
8. Run backend/unit/integration checks.
9. Run at least one end-to-end incident through the agent.
10. Fix integration failures before continuing.

## Exit Criteria

A local incident can be created, investigated through real tools backed by the simulator, and produce evidence/hypotheses/root-cause output.
