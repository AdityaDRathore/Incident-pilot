# Tool Contracts

All tools must conform to strict schemas and provide standard metadata for the policy engine.

## Base Tool Schema
Each tool is a callable class/function with the following metadata:
- `name`: string (e.g., `query_metrics`)
- `description`: string (Detailed instructions for the LLM)
- `input_schema`: Pydantic model
- `output_schema`: Pydantic model
- `risk_level`: `READ_ONLY`, `LOW`, `MEDIUM`, `CRITICAL`
- `requires_approval`: bool
- `allowed_roles`: List[str]

## Diagnostic Tools (Read-Only)
- `search_logs(service: str, query: str, time_window: str) -> List[str]`
- `query_metrics(service: str, metric: str, time_window: str) -> List[DataPoint]`
- `get_service_health(service: str) -> HealthStatus`
- `get_recent_deployments(service: str, limit: int) -> List[Deployment]`
- `search_runbooks(query: str) -> List[Chunk]`

## Remediation Tools (Mutating)
- `restart_service(service: str) -> Result`
  - Risk: LOW
  - Requires Approval: True
- `rollback_deployment(service: str, to_version: str) -> Result`
  - Risk: MEDIUM
  - Requires Approval: True
- `scale_service(service: str, replicas: int) -> Result`
  - Risk: LOW
  - Requires Approval: True
