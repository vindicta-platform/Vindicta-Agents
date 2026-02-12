"""Nexus Module
=============

The top-level orchestrator graph ("Nexus") that composes the planning
and execution sub-graphs into a single executable workflow:

    PlanningPhase → HumanReview → ExecutionPhase → END

A hard interrupt is inserted before ExecutionPhase so a human can
inspect and approve the generated task list before domain agents run.
"""

from typing import Any, Dict

from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from .state import VindictaState
from .meta_graph import meta_graph
from .domain_graph import domain_graph
from ..utils.logger import logger

def human_review_node(state: VindictaState) -> Dict[str, Any]:
    """Breakpoint node for human-in-the-loop review.

    Logs the number of pending tasks and returns an empty dict
    (no state mutations).  The actual pause is enforced by the
    ``interrupt_before`` parameter in :func:`build_master_graph`.
    """
    logger.info("human_review_phase_initiated", task_count=len(state.get('tasks', [])))
    return {}

def build_master_graph() -> Any:
    """Construct and compile the top-level Nexus graph.

    Returns:
        CompiledStateGraph: The executable master graph with a
        human-in-the-loop interrupt before the execution phase.
    """
    master_builder = StateGraph(VindictaState)

    master_builder.add_node("PlanningPhase", meta_graph)
    master_builder.add_node("HumanReview", human_review_node)
    master_builder.add_node("ExecutionPhase", domain_graph)

    master_builder.set_entry_point("PlanningPhase")
    master_builder.add_edge("PlanningPhase", "HumanReview")
    master_builder.add_edge("HumanReview", "ExecutionPhase")
    master_builder.add_edge("ExecutionPhase", END)

    memory = MemorySaver()

    return master_builder.compile(
        checkpointer=memory,
        interrupt_before=["ExecutionPhase"],
    )

# Export the compiled swarm instance
vindicta_swarm = build_master_graph()
