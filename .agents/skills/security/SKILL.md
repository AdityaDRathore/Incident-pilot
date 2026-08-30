---
name: security
description: Attack the complete application and harden it.
---

# IncidentPilot Security Review

## Description
Attack the complete application and harden it.

## Steps

1. Delegate to `incidentpilot-security`.
2. Give it repository-wide inspection access.
3. Require reproducible tests for all findings.
4. Attack:
   - prompt injection
   - malicious runbooks
   - malicious logs
   - unauthorized tool calls
   - RBAC bypass
   - approval bypass
   - dangerous action escalation
   - unrestricted SQL/shell pathways
   - secret leakage
   - infinite loops
5. Apply fixes.
6. Re-run every exploit.
7. Review threat model.
8. Run the complete security suite.

## Exit Criteria

No known Critical/High findings remain, required security regression tests pass, and protected actions cannot bypass deterministic policy.
