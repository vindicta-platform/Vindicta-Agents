# How to Delegate Tasks to the Swarm

The Vindicta Swarm uses a unified state object (`VindictaState`) to route tasks to specific domain agents. This guide details how to construct requests and delegate work.

## 1. The State Structure

The core unit of work is a `Task` object within the `VindictaState`.

```python
state = {
    "intent": "High-level goal (e.g., 'Update the portal')",
    "tasks": [
        {
            "id": "unique-uuid",
            "description": "Detailed instruction for the agent",
            "target_realm": "target-domain-key",  # <-- CRITICAL for routing
            "status": "pending"
        }
    ],
    # ... other fields are managed by the swarm
}
```

## 2. Target Realms

Use these exact keys for `target_realm` to route tasks to the correct agent:

| Realm Key          | Agent Name     | Repository         | Tech Stack |
| ------------------ | -------------- | ------------------ | ---------- |
| `vindicta-engine`  | TechPriest     | Vindicta-Engine    | Python     |
| `warscribe-system` | LogosHistorian | WarScribe-System   | Python     |
| `vindicta-economy` | VoidBanker     | Vindicta-Economy   | Python     |
| `primordia-ai`     | SeersOracle    | Primordia-AI       | Python     |
| `meta-oracle`      | DebateMaster   | Meta-Oracle        | Python     |
| `logi-slate-ui`    | ForgeSmith     | Logi-Slate-UI      | Node/TS    |
| `vindicta-portal`  | PortalArchon   | Vindicta-Portal    | JS/Vite    |
| `vindicta-api`     | GateKnight     | Vindicta-API       | Python     |

## 3. Python Execution Example

To programmatically delegate a task (e.g., from a script or pipeline):

```python
import uuid
from vindicta_agents.swarm.domain_graph import domain_graph

# 1. Define the Work
task_payload = {
    "intent": "Update Portal Hero Section",
    "tasks": [
        {
            "id": str(uuid.uuid4()),
            "description": "Change hero text to 'Welcome to the 41st Millennium'",
            "target_realm": "vindicta-portal",
            "status": "pending"
        }
    ]
}

# 2. Invoke the Swarm
print("Dispatching task to PortalArchon...")
result = domain_graph.invoke(task_payload)

# 3. Check Results
logs = result.get("execution_log", [])
print("\n".join(logs))
```

## 4. CLI / Chat Delegation (Future)

*Currently, delegation is done via code (scripts) or the `demo_grand_tour.py` harness.*

In the future, you will be able to type naturally:
> "Ask ForgeSmith to add a fuel gauge to the logistics dashboard."

The **Meta-Agents** (Product Owner -> Architect -> Delivery Lead) will automatically:
1.  Parse your intent.
2.  Slice it into a task.
3.  Set `target_realm="logi-slate-ui"`.
4.  Dispatch to the swarm.
