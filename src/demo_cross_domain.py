import json
import sys
import os
sys.path.append(os.path.join(os.getcwd(), "src"))
from vindicta_agents.swarm.domain_graph import task_router, domain_graph
from vindicta_agents.swarm.domain_registry import DOMAIN_REGISTRY
from vindicta_agents.swarm.state import VindictaState

def run_demo():
    print("=== Vindicta Cross-Domain Swarm Demo ===\n")
    
    # 1. Someone asks for an AI-related update (Primordia-AI)
    intent = "Analyze the latest seers logic in Primordia-AI"
    print(f"User Intent: {intent}")
    
    # 2. The swarm generates a task targeting the 'primordia-ai' realm
    state: VindictaState = {
        "intent": intent,
        "tasks": [
            {
                "id": "task-seer-1",
                "description": "Refactor heuristic evaluator in Primordia-AI",
                "target_realm": "primordia-ai",
                "status": "pending"
            }
        ],
        "target_realms": [],
        "execution_log": [],
        "current_phase": "planning"
    }
    
    # 3. The Router looks at the task and chooses the right "Room" (Node)
    next_nodes = task_router(state)
    print(f"\n[Router] Task detected for 'primordia-ai'.")
    print(f"[Router] Routing to Swarm Node: {next_nodes}")
    
    # 4. We check our "Master Map" (Registry) to see where that room is
    realm_info = DOMAIN_REGISTRY.get("primordia-ai")
    print(f"\n[Registry] Looking up metadata for 'primordia-ai'...")
    print(f" - Repository: {realm_info['repo_name']}")
    print(f" - Tech Stack: {realm_info['tech_stack']}")
    print(f" - Primary Language: {realm_info['primary_language']}")
    
    # 5. The Swarm Node "activates" (Simulated)
    print("\n[Execution] Activating SeersOracle Node...")
    # Using the actual graph call would trigger logging
    final_state = domain_graph.invoke(state)
    
    print("\n[Success] Final Execution Log:")
    for log in final_state.get('execution_log', []):
        print(f" - {log}")

if __name__ == "__main__":
    run_demo()
