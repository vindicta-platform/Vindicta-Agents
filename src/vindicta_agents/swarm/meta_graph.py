from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableConfig
from .state import VindictaState
from vindicta_agents.sdk.models import AITask
from .config import MockLLMProvider


def product_owner_node(state: VindictaState, config: RunnableConfig):
    configurable = config.get("configurable", {})
    provider = configurable.get("llm_provider", MockLLMProvider())

    task = AITask(
        name="Spec Creation",
        system="You are the PO.",
        prompt=f"Write a spec for: {state['intent']}",
    )
    return {"spec_content": task.execute(provider=provider), "current_phase": "planning"}


def architect_node(state: VindictaState, config: RunnableConfig):
    configurable = config.get("configurable", {})
    provider = configurable.get("llm_provider", MockLLMProvider())

    spec = state.get("spec_content", "")
    task = AITask(
        name="Plan Creation",
        system="You are the Architect.",
        prompt=f"Draft a plan based on this spec:\n{spec}",
    )
    return {"plan_content": task.execute(provider=provider)}


def adl_node(state: VindictaState, config: RunnableConfig):
    configurable = config.get("configurable", {})
    provider = configurable.get("llm_provider", MockLLMProvider())

    plan = state.get("plan_content", "")
    task = AITask(
        name="Task Slicing",
        system="You are the Agile Delivery Lead. Output a JSON list of tasks, assigning each to a target_realm (e.g., vindicta-engine).",
        prompt=plan,
    )
    tasks_json = task.execute_json(provider=provider)
    return {"tasks": tasks_json, "current_phase": "review"}


def build_meta_graph():
    meta_builder = StateGraph(VindictaState)
    meta_builder.add_node("PO", product_owner_node)
    meta_builder.add_node("Architect", architect_node)
    meta_builder.add_node("ADL", adl_node)

    meta_builder.set_entry_point("PO")
    meta_builder.add_edge("PO", "Architect")
    meta_builder.add_edge("Architect", "ADL")
    meta_builder.add_edge("ADL", END)

    return meta_builder.compile()


# Export compiled instance
meta_graph = build_meta_graph()
