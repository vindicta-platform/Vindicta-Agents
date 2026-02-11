from typing import TypedDict, Annotated, List, Dict, Optional
import operator

class Task(TypedDict):
    id: str
    description: str
    target_realm: str # e.g., 'vindicta-engine', 'warscribe-system'
    status: str       # 'pending', 'in-progress', 'completed', 'failed'
    code_diff: Optional[str]    # The actual code written by the Domain Agent

class VindictaState(TypedDict):
    # Top-Level Context
    intent: str
    
    # SDD Lifecycle State (Meta-Agents)
    spec_content: Optional[str]
    plan_content: Optional[str]
    
    # Execution State (Domain Agents)
    tasks: Annotated[List[Task], operator.add]
    
    # Routing & Control
    current_phase: str # 'planning', 'review', 'execution', 'done'
    error_log: Optional[str]
    execution_log: Annotated[List[str], operator.add]
