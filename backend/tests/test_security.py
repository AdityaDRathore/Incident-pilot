import pytest
from app.policies.engine import check_tool_permission, AuthError, SecurityError, RiskLevel
from app.tools.definitions import execute_with_policy
from app.simulation import simulator
import json

def test_rbac_viewer_cannot_execute_tools(monkeypatch):
    """Test that a VIEWER role cannot execute diagnostic or remediation tools."""
    import app.tools.definitions as definitions
    monkeypatch.setattr(definitions, "CURRENT_USER_ROLE", "VIEWER")
    
    with pytest.raises(AuthError):
        definitions.execute_with_policy("search_logs", RiskLevel.READ_ONLY, False, ["ENGINEER", "ADMIN"], 
                            simulator.search_logs, "test-incident", "checkout-api")

def test_rbac_engineer_can_read():
    """Test that an ENGINEER role can execute diagnostic tools."""
    res = execute_with_policy("search_logs", RiskLevel.READ_ONLY, False, ["ENGINEER", "ADMIN"], 
                              simulator.search_logs, "test-incident", "checkout-api")
    assert res is not None

def test_approval_bypass_prevention():
    """Test that defining a DANGEROUS tool without requiring approval throws a SecurityError."""
    with pytest.raises(SecurityError, match="marked high risk but does not require approval"):
        check_tool_permission("ADMIN", "delete_database", RiskLevel.CRITICAL.value, False, ["ADMIN"])

def test_unrestricted_sql_shell_defense():
    """
    Test that there are no arbitrary shell/SQL tools.
    In our architecture, tools are strictly typed. We assert that only predefined safe/dangerous tools exist.
    """
    from app.tools.definitions import ALL_TOOLS
    tool_names = [t.name for t in ALL_TOOLS]
    assert "execute_shell" not in tool_names
    assert "execute_sql" not in tool_names

def test_malicious_runbook_prompt_injection():
    """
    Simulate retrieving a malicious runbook and verify that even if the LLM is tricked,
    the policy engine prevents unauthorized execution of dangerous tools like 'delete_database'.
    """
    from app.retrieval.rag import MOCK_RUNBOOKS, search_runbooks
    
    # 1. Verify the malicious runbook exists in our RAG
    malicious_runbooks = [rb for rb in MOCK_RUNBOOKS if "IGNORE ALL PREVIOUS INSTRUCTIONS" in rb["content"]]
    assert len(malicious_runbooks) > 0
    
    # 2. Even if the LLM outputted a tool call to 'delete_database', it would fail at the policy layer.
    with pytest.raises(AuthError):
        # We simulate the LLM attempting to call a fake dangerous tool it shouldn't have access to
        check_tool_permission("ENGINEER", "delete_database", RiskLevel.CRITICAL.value, True, ["ADMIN"])

def test_infinite_loop_prevention():
    """
    LangGraph provides recursion limits to prevent infinite loops.
    We test that setting recursion_limit stops an out-of-control agent.
    """
    from langgraph.graph import StateGraph, END
    from langgraph.errors import GraphRecursionError
    
    # Create a dummy looping graph
    workflow = StateGraph(dict)
    workflow.add_node("loop", lambda x: x)
    workflow.set_entry_point("loop")
    workflow.add_edge("loop", "loop")
    app = workflow.compile()
    
    with pytest.raises(GraphRecursionError):
        app.invoke({}, config={"recursion_limit": 5})

