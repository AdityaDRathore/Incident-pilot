# Event Contracts

Events are used to push real-time updates to the frontend via SSE or WebSockets.

## Event Schema
```json
{
  "event": "event_type",
  "incident_id": "uuid",
  "timestamp": "iso8601",
  "data": { ... }
}
```

## Standard Events
- `incident.created`: A new incident was logged.
- `agent.started`: Agent workflow kicked off.
- `agent.phase_changed`: `data: { old_phase, new_phase }`
- `tool.started`: `data: { tool_name, arguments }`
- `tool.completed`: `data: { tool_name, result, status }`
- `evidence.created`: `data: { evidence_id, content, relevance }`
- `hypothesis.updated`: `data: { hypothesis_id, status, confidence }`
- `approval.required`: `data: { action_type, target, risk_level }`
- `remediation.started`: Agent is executing an approved action.
- `remediation.completed`: Action finished.
- `incident.resolved`: Root cause verified and fixed.
- `incident.failed`: Max loops/budget hit without resolution.
