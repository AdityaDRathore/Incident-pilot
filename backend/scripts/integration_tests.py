import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.simulation.simulator import initialize_incident, get_simulator
from app.graph.workflow import app
from langchain_core.messages import HumanMessage, AIMessage

def mock_llm_for_integration(state):
    """
    Since we do not require a real LLM for the integration test script,
    we can manually inject tool calls into the state to test the graph's deterministic safety and pause/resume logic.
    This proves the architecture connects correctly.
    """
    messages = state["messages"]
    incident = state["incident"]
    
    # We will look at what was previously said. 
    # If the last message is just the start, we'll ask to search logs.
    if len(messages) == 1:
        msg = AIMessage(content="I will search logs.")
        msg.tool_calls = [{"name": "search_logs", "args": {"service": "checkout-api"}, "id": "call_1"}]
        return {"messages": [msg]}
    
    if len(messages) == 3:
        if "bad-deployment" in incident:
            msg = AIMessage(content="Logs show a failure. I will rollback the deployment.")
            msg.tool_calls = [{"name": "rollback_deployment", "args": {"service": "checkout-api", "to_version": "v2.8.0"}, "id": "call_2"}]
        elif "redis-outage" in incident:
            msg = AIMessage(content="Redis connection refused. I will restart redis.")
            msg.tool_calls = [{"name": "restart_service", "args": {"service": "redis"}, "id": "call_2"}]
        else:
            msg = AIMessage(content="Pool exhausted. I will restart the service.")
            msg.tool_calls = [{"name": "restart_service", "args": {"service": "checkout-api"}, "id": "call_2"}]
        return {"messages": [msg]}
        
    return {"messages": [AIMessage(content="Investigation complete.")]}

def test_scenario(scenario_name, incident_id):
    print(f"\n=============================================")
    print(f"🔄 Running Scenario: {scenario_name}")
    print(f"=============================================")
    
    initialize_incident(incident_id, scenario_name)
    
    # We monkeypatch the agent_node for this test to forcefully drive the deterministic graph
    # without needing real OpenAI credits.
    import app.graph.workflow
    original_agent_node = app.graph.workflow.agent_node
    app.graph.workflow.agent_node = mock_llm_for_integration
    
    # We must recompile the graph because we changed the function
    from langgraph.graph import StateGraph, END
    from langgraph.prebuilt import ToolNode
    from langgraph.checkpoint.memory import MemorySaver
    from app.tools.definitions import ALL_TOOLS
    from app.graph.workflow import should_continue, GraphState
    
    workflow = StateGraph(GraphState)
    workflow.add_node("agent", mock_llm_for_integration)
    workflow.add_node("safe_action", ToolNode(ALL_TOOLS))
    workflow.add_node("dangerous_action", ToolNode(ALL_TOOLS))
    workflow.set_entry_point("agent")
    workflow.add_conditional_edges(
        "agent", 
        should_continue, 
        {
            "safe_action": "safe_action", 
            "dangerous_action": "dangerous_action",
            "end": END
        }
    )
    workflow.add_edge("safe_action", "agent")
    workflow.add_edge("dangerous_action", "agent")
    memory = MemorySaver()
    test_app = workflow.compile(checkpointer=memory, interrupt_before=["dangerous_action"])

    config = {"configurable": {"thread_id": incident_id}}
    
    inputs = {
        "messages": [HumanMessage(content="Start investigation")],
        "incident": f"Test {scenario_name}",
        "phase": "INVESTIGATING"
    }

    print("\n▶️ Start Graph Execution...")
    for output in test_app.stream(inputs, config=config):
        for key, value in output.items():
            print(f"Node -> {key}")
            if "messages" in value:
                print(f"Message: {value['messages'][-1].content}")
                
    # Check if we hit the pause
    state = test_app.get_state(config)
    if state.next:
        print(f"\n⏸️ Graph Paused. Awaiting human approval for nodes: {state.next}")
        
        # We approve the action by continuing the graph
        print("\n✅ Human Approval Granted. Resuming...")
        
        for output in test_app.stream(None, config=config):
            for key, value in output.items():
                print(f"Node -> {key}")
                if "messages" in value:
                    print(f"Message: {value['messages'][-1].content}")
    else:
        print("\n⚠️ Graph did not pause. Something went wrong.")

    # Verify telemetry changes
    sim = get_simulator(incident_id)
    print(f"\n📊 Final Telemetry for checkout-api:")
    print(f"Status: {sim.services['checkout-api']['status']}")
    print(f"Error Rate: {sim.metrics['checkout-api'].get('error_rate', 0)}")
    
    if sim.services['checkout-api']['status'] == 'healthy':
        print("\n🎉 Incident successfully remediated!")
    else:
        print("\n❌ Incident remediation failed.")

if __name__ == "__main__":
    test_scenario("bad-deployment", "test-incident")
    test_scenario("db-pool-exhaustion", "test-incident")
    test_scenario("redis-outage", "test-incident")
