import sys
import os
import uuid

# Ensure we can find the src package
sys.path.append(os.path.join(os.getcwd(), "src"))

from vindicta_agents.swarm.domain_graph import domain_graph
from vindicta_agents.swarm.domain_registry import DOMAIN_REGISTRY
from vindicta_agents.swarm.state import VindictaState

def run_grand_tour():
    print("===============================================================")
    print("      🚀 VINDICTA SWARM: THE GRAND TOUR (8-REALM DEMO)       ")
    print("===============================================================\n")

    # Define a task for every single domain in the registry
    demo_tasks = [
        {
            "realm": "vindicta-engine",
            "intent": "Optimize the DiceEngine probability matrix",
            "task_desc": "Refactor entropy pool for true randomness"
        },
        {
            "realm": "warscribe-system",
            "intent": "Archive the latest Battle Report",
            "task_desc": "Parse and store combat logs in immutable ledger"
        },
        {
            "realm": "vindicta-economy",
            "intent": "Audit the Void Bank logic",
            "task_desc": "Calculate resource inflation rates"
        },
        {
            "realm": "primordia-ai",
            "intent": "Upgrade Seers Oracle heuristics",
            "task_desc": "Enhance predictive combat models"
        },
        {
            "realm": "meta-oracle",
            "intent": "Mediating a rules debate",
            "task_desc": "Resolve conflict between RAW and RAI interpretation"
        },
        {
            "realm": "logi-slate-ui",
            "intent": "Update the Logistics Dashboard",
            "task_desc": "Add new widgets for resource tracking"
        },
        {
            "realm": "vindicta-portal",
            "intent": "Refresh the Portal Landing Page",
            "task_desc": "Implement new hero section with 3D assets"
        },
        {
            "realm": "vindicta-api",
            "intent": "Expose new GraphQL endpoints",
            "task_desc": "Create resolvers for new agent telemetry"
        }
    ]

    for i, item in enumerate(demo_tasks, 1):
        realm_key = item["realm"]
        intent = item["intent"]
        task_desc = item["task_desc"]
        
        # 1. Lookup Metadata
        registry_info = DOMAIN_REGISTRY.get(realm_key, {})
        repo_name = registry_info.get("repo_name", "UNKNOWN")
        tech_stack = registry_info.get("tech_stack", "UNKNOWN")

        print(f"[{i}/8] Processing Request for: {realm_key.upper()}")
        print(f"      Target Repo: {repo_name} | Stack: {tech_stack}")
        print(f"      User Intent: '{intent}'")
        
        # 2. Construct State
        state: VindictaState = {
            "intent": intent,
            "tasks": [
                {
                    "id": str(uuid.uuid4()),
                    "description": task_desc,
                    "target_realm": realm_key,
                    "status": "pending"
                }
            ],
            "target_realms": [],
            "execution_log": [],
            "current_phase": "planning"
        }

        # 3. Invoke Swarm
        try:
            # We use invoke to actually run the graph
            final_state = domain_graph.invoke(state)
            
            # 4. Parse Results
            logs = final_state.get("execution_log", [])
            if logs:
                print(f"      ✅ SUCCESS: Swarm responded with: {logs[0]}")
            else:
                 print(f"      ❌ FAILED: No execution log returned.")
        except Exception as e:
            print(f"      ❌ ERROR: {e}")
        
        print("-" * 60)

if __name__ == "__main__":
    run_grand_tour()
