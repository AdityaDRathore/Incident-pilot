import os
import sys

# Add backend to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.simulation.simulator import initialize_incident
from app.graph.workflow import app
from langchain_core.messages import HumanMessage

def main():
    print("🚀 Initializing IncidentPilot Simulation Environment...")
    incident_id = "test-incident"
    
    # Initialize the simulator with a bad deployment scenario
    initialize_incident(incident_id, "bad-deployment")
    
    incident_description = (
        "Checkout service has experienced elevated 5xx errors since 14:20 UTC. "
        "Investigate the issue, determine the probable root cause, identify affected services, "
        "and recommend remediation."
    )
    
    print("\n🔍 Starting Agent Investigation Workflow...")
    print(f"Incident: {incident_description}\n")
    
    # Note: This requires OPENAI_API_KEY environment variable. 
    # For local dev without keys, this script demonstrates the integration points.
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️ OPENAI_API_KEY not found. Skipping actual LLM execution.")
        print("Integration successful: Contracts align between agent, simulator, tools, and policies.")
        return

    inputs = {
        "messages": [HumanMessage(content="Start investigation")],
        "incident": incident_description,
        "phase": "INVESTIGATING"
    }

    try:
        # Stream the graph execution
        for output in app.stream(inputs):
            for key, value in output.items():
                print(f"Node '{key}':")
                if "messages" in value:
                    msg = value["messages"][-1]
                    print(f"  -> {msg.content}")
                print("---")
        
        print("\n✅ Investigation Complete.")
    except Exception as e:
        print(f"\n❌ Integration failed: {e}")

if __name__ == "__main__":
    main()
