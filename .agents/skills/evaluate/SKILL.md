---
name: evaluate
description: Measure whether the complete agent actually works.
---

# IncidentPilot Evaluation

## Description
Measure whether the complete agent actually works.

## Steps

1. Delegate to `incidentpilot-evaluation`.
2. Confirm benchmark contains at least 50 deterministic tasks.
3. Run full or configured evaluation.
4. Measure:
   - task success
   - root-cause accuracy
   - evidence correctness
   - tool selection
   - hallucination
   - remediation correctness
   - approval compliance
   - prompt-injection resistance
   - recovery verification
   - latency
   - tool calls
   - estimated cost
5. Save raw results.
6. Generate aggregate report.
7. Identify worst failures.
8. Route failures back to the appropriate agent.
9. Re-run targeted cases.
10. Compare baseline/current results.
11. Never fabricate values.

## Exit Criteria

Evaluation results are reproducible, stored, and useful for identifying concrete engineering improvements.
