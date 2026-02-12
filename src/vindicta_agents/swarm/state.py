"""Swarm State Definitions
========================

Canonical state schema shared by all sub-graphs in the Vindicta Swarm.
LangGraph merges partial updates from each node using the ``Annotated``
reducers defined here (e.g. ``operator.add`` for list accumulation).
"""

import operator
from typing import Annotated, List, Optional, TypedDict

class Task(TypedDict):
    """A discrete unit of work assigned to a domain agent."""

    id: str
    description: str
    target_realm: str  # e.g. 'vindicta-engine', 'warscribe-system'
    status: str        # 'pending' | 'in-progress' | 'completed' | 'failed'
    code_diff: Optional[str]

class VindictaState(TypedDict):
    """Top-level state flowing through the Vindicta Swarm graph."""

    # --- Context ---
    intent: str

    # --- Planning (Meta-Agents) ---
    spec_content: Optional[str]
    plan_content: Optional[str]

    # --- Execution (Domain Agents) ---
    tasks: Annotated[List[Task], operator.add]

    # --- Routing & Observability ---
    current_phase: str  # 'planning' | 'review' | 'execution' | 'done'
    error_log: Optional[str]
    execution_log: Annotated[List[str], operator.add]
