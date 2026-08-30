from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime
import uuid

class Evidence(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    source: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    type: str
    content: str
    relevance: str
    tool_used: str

class Hypothesis(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    description: str
    confidence: float
    supporting_evidence_ids: List[str] = Field(default_factory=list)
    contradicting_evidence_ids: List[str] = Field(default_factory=list)
    status: str = "OPEN" # OPEN, SUPPORTED, WEAKENED, REJECTED, CONFIRMED
    next_steps: str = ""

class ToolCallRecord(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    tool_name: str
    arguments: Dict[str, Any]
    status: str = "PENDING"
    result: Optional[str] = None
    error: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class ActionRequest(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    action_type: str
    target: str
    risk_level: str
    justification: str
    status: str = "PENDING" # PENDING, APPROVED, REJECTED
    evidence_ids: List[str] = Field(default_factory=list)

class AgentState(BaseModel):
    incident_id: str
    # Cannot store raw LangChain AIMessage in Pydantic easily without arbitrary_types_allowed,
    # so we will store them as dicts or use LangGraph's built-in message state handling.
    # For now, we rely on LangGraph's MessageGraph or typed dictionary state.
    messages: List[Dict[str, Any]] = Field(default_factory=list)
    current_phase: str = "INTAKE" 
    
    investigation_plan: str = ""
    evidence: List[Evidence] = Field(default_factory=list)
    hypotheses: List[Hypothesis] = Field(default_factory=list)
    tool_calls: List[ToolCallRecord] = Field(default_factory=list)
    
    selected_root_cause: Optional[str] = None
    root_cause_confidence: float = 0.0
    
    approval_request: Optional[ActionRequest] = None
    remediation_result: Optional[str] = None
    verification_result: Optional[str] = None
    
    errors: List[str] = Field(default_factory=list)
    retry_count: int = 0
    budget_used: float = 0.0
