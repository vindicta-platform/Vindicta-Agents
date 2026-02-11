from langgraph.graph import StateGraph, END
from .state import VindictaState
# Assuming you wrap your LLM calls in a utility
from vindicta_agents.sdk.models import AITask 

def product_owner_node(state: VindictaState):
    task = AITask(
        name="Spec Creation",
        system="You are the PO.", 
        prompt=f"Write a spec for: {state['intent']}"
    )
    return {"spec_content": task.execute(), "current_phase": "planning"}

def architect_node(state: VindictaState):
    spec = state.get('spec_content', "")
    task = AITask(
        name="Plan Creation",
        system="You are the Architect.", 
        prompt=f"Draft a plan based on this spec:\n{spec}"
    )
    return {"plan_content": task.execute()}

def adl_node(state: VindictaState):
    plan = state.get('plan_content', "")
    # The ADL reads the plan and generates JSON tasks, specifically assigning the "target_realm"
    task = AITask(
        name="Task Slicing",
        system="You are the Agile Delivery Lead. Output a JSON list of tasks, assigning each to a target_realm (e.g., vindicta-engine).", 
        prompt=plan
    )
    tasks_json = task.execute_json() # Assumes a method that forces JSON output
    return {"tasks": tasks_json, "current_phase": "review"}

# Build the Meta-Graph
meta_builder = StateGraph(VindictaState)
meta_builder.add_node("PO", product_owner_node)
meta_builder.add_node("Architect", architect_node)
meta_builder.add_node("ADL", adl_node)

meta_builder.set_entry_point("PO")
meta_builder.add_edge("PO", "Architect")
meta_builder.add_edge("Architect", "ADL")
meta_builder.add_edge("ADL", END)

meta_graph = meta_builder.compile()
