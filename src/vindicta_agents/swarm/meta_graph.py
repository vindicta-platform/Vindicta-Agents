"""
Meta Graph Module
=================

This module defines the high-level planning graph for the Vindicta Swarm.
It orchestrates the transformation of a user intent into an executable task list via a chain of specialized AI agents.

The graph is constructed dynamically from a configuration registry persisted in JSON,
allowing for easier adjustment of prompts and agent flows.
"""

import json
import pathlib
from typing import Any, Dict, List, Optional, TypedDict, Callable
from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableConfig

from .state import VindictaState
from vindicta_agents.sdk.models import AITask
from .config import MockLLMProvider


class AgentConfig(TypedDict, total=False):
    """Configuration for a planning agent node."""
    task_name: str
    system_prompt: str
    input_key: str
    output_key: str
    prompt_template: str
    phase_update: Optional[str]
    json_mode: bool


# --- Loading Configuration ---

_PLANNING_CONFIG_PATH = pathlib.Path(__file__).parent / "configs" / "planning_agents.json"

def _load_planning_agents() -> Dict[str, AgentConfig]:
    with open(_PLANNING_CONFIG_PATH, "r") as f:
        return json.load(f)

PLANNING_AGENTS: Dict[str, AgentConfig] = _load_planning_agents()


# --- Generic Planning Node Factory ---

def make_planning_node(agent_id: str) -> Callable[[VindictaState, RunnableConfig], Dict[str, Any]]:
    """
    Creates a LangGraph node function for a specific planning agent.

    Args:
        agent_id: The key of the agent in PLANNING_AGENTS (e.g., 'PO', 'ADL').

    Returns:
        Callable: A function matching the Node signature (state, config) -> dict.
    """
    config_data = PLANNING_AGENTS.get(agent_id)
    if not config_data:
        raise ValueError(f"Unknown agent_id: {agent_id}")

    task_name = config_data["task_name"]
    system_prompt = config_data["system_prompt"]
    input_key = config_data["input_key"]
    output_key = config_data["output_key"]
    prompt_template = config_data["prompt_template"]
    phase_update = config_data.get("phase_update")
    json_mode = config_data.get("json_mode", False)

    def planning_node(state: VindictaState, config: RunnableConfig) -> Dict[str, Any]:
        configurable = config.get("configurable", {})
        provider = configurable.get("llm_provider", MockLLMProvider())

        input_value = state.get(input_key, "")  # type: ignore
        
        task = AITask(
            name=task_name,
            system=system_prompt,
            prompt=prompt_template.format(input=input_value),
        )

        updates: Dict[str, Any] = {}
        
        if json_mode:
            result_json = task.execute_json(provider=provider)
            updates[output_key] = result_json
        else:
            result_text = task.execute(provider=provider)
            updates[output_key] = result_text

        if phase_update:
            updates["current_phase"] = phase_update

        return updates

    # Set metadata
    planning_node.__name__ = f"{agent_id.lower()}_node"
    return planning_node


# --- Graph Construction ---

def build_meta_graph() -> Any:
    """
    Constructs and compiles the StateGraph for the planning layer.

    Returns:
        CompiledStateGraph: The executable LangGraph.
    """
    meta_builder = StateGraph(VindictaState)

    # 1. Add Nodes
    nodes = ["PO", "Architect", "ADL"]
    for agent_id in nodes:
        meta_builder.add_node(agent_id, make_planning_node(agent_id))

    # 2. Add Edges (Linear Flow)
    meta_builder.set_entry_point("PO")
    meta_builder.add_edge("PO", "Architect")
    meta_builder.add_edge("Architect", "ADL")
    meta_builder.add_edge("ADL", END)

    return meta_builder.compile()


# Export compiled instance
meta_graph = build_meta_graph()

# --- Backward Compatibility ---
product_owner_node = make_planning_node("PO")
architect_node = make_planning_node("Architect")
adl_node = make_planning_node("ADL")
