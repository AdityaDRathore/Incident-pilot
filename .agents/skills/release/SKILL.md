---
name: release
description: Run complete QA, build, security, evaluation, Docker, and documentation checks.
---

# IncidentPilot Release Gate

## Description
Run complete QA, build, security, evaluation, Docker, and documentation checks.

## Steps

1. Delegate to `incidentpilot-release`.
2. Run all quality gates.
3. Build backend and frontend.
4. Build Docker images.
5. Start a clean Docker Compose environment.
6. Run end-to-end scenarios.
7. Verify HITL.
8. Verify audit trail.
9. Verify security suite.
10. Run evaluation smoke test.
11. Review README and docs.
12. Create `docs/final-review.md`.
13. Fix any failed gate.
14. Re-run the failed gate and all affected tests.
15. Only recommend release when required gates pass.

## Exit Criteria

The repository is reproducible, tested, documented, and ready for portfolio demonstration.
