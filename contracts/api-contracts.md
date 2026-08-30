# API Contracts

The backend provides a RESTful API via FastAPI.

## Incident Management
- `POST /api/incidents`: Create a new incident. (Body: title, description, severity, service)
- `GET /api/incidents`: List incidents (supports filters).
- `GET /api/incidents/{id}`: Get full incident details.

## Agent Execution
- `POST /api/incidents/{id}/investigate`: Start the agent workflow asynchronously.
- `GET /api/incidents/{id}/timeline`: Retrieve timeline of agent and system events.
- `GET /api/incidents/{id}/evidence`: Retrieve gathered evidence.
- `GET /api/incidents/{id}/hypotheses`: Retrieve active/resolved hypotheses.

## Human-in-the-Loop
- `POST /api/incidents/{id}/approve`: Approve a pending action request, unpausing the graph.
- `POST /api/incidents/{id}/reject`: Reject an action request, unpausing the graph.
- `POST /api/incidents/{id}/cancel`: Cancel the entire investigation.

## Telemetry
- `GET /api/agent-runs/{id}`: Detailed trace of LLM calls, latency, and cost for a run.
- `GET /api/health`: Standard health check.
