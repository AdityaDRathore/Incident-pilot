# Agent State Contract

The LangGraph state will use a Pydantic model (`AgentState`) to ensure type safety across all nodes.

```python
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime

class Evidence(BaseModel):
    id: str
    source: str
    timestamp: datetime
    type: str
    content: str
    relevance: str
    tool_used: str

class Hypothesis(BaseModel):
    id: str
    description: str
    confidence: float
    supporting_evidence_ids: List[str]
    contradicting_evidence_ids: List[str]
    status: str # OPEN, SUPPORTED, WEAKENED, REJECTED, CONFIRMED
    next_steps: str

class ToolCall(BaseModel):
    id: str
    tool_name: str
    arguments: Dict[str, Any]
    status: str # PENDING, SUCCESS, FAILED, DENIED
    result: Optional[str]
    error: Optional[str]
    timestamp: datetime

class ActionRequest(BaseModel):
    id: str
    action_type: str
    target: str
    risk_level: str
    justification: str
    status: str # PENDING, APPROVED, REJECTED
    evidence_ids: List[str]

class AgentState(BaseModel):
    incident_id: str
    messages: List[Any] # LangChain messages
    current_phase: str # INTAKE, INVESTIGATING, HYPOTHESIZING, AWAITING_APPROVAL, REMEDIATING, VERIFYING, RESOLVED, FAILED
    
    investigation_plan: str = ""
    evidence: List[Evidence] = Field(default_factory=list)
    hypotheses: List[Hypothesis] = Field(default_factory=list)
    tool_calls: List[ToolCall] = Field(default_factory=list)
    
    selected_root_cause: Optional[str] = None
    root_cause_confidence: float = 0.0
    
    approval_request: Optional[ActionRequest] = None
    remediation_result: Optional[str] = None
    verification_result: Optional[str] = None
    
    errors: List[str] = Field(default_factory=list)
    retry_count: int = 0
    budget_used: float = 0.0
```
