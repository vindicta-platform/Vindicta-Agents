from langgraph.graph import StateGraph, END
from .state import VindictaState
from ..utils.logger import logger

def setup_execution_node(state: VindictaState):
    logger.info("execution_phase_initializing")
    return {"current_phase": "execution"}

# --- Domain Node Implementations ---
def tech_priest_node(state: VindictaState):
    # Filters state['tasks'] for target_realm == 'vindicta-engine'
    logger.info("tech_priest_activated", realm="vindicta-engine")
    return {"execution_log": ["TechPriest activated"]}

def logos_historian_node(state: VindictaState):
    # Filters for target_realm == 'warscribe-system'
    logger.info("logos_historian_activated", realm="warscribe-system")
    return {"execution_log": ["LogosHistorian activated"]}

def void_banker_node(state: VindictaState):
    # Filters for target_realm == 'vindicta-economy'
    logger.info("void_banker_activated", realm="vindicta-economy")
    return {"execution_log": ["VoidBanker activated"]}

# --- The Router ---
def task_router(state: VindictaState):
    # Looks at the pending tasks and returns a list of nodes to activate in parallel
    tasks = state.get('tasks', [])
    active_realms = set(t['target_realm'] for t in tasks if t.get('status') == 'pending')
    
    routes = []
    if 'vindicta-engine' in active_realms: routes.append("TechPriest")
    if 'warscribe-system' in active_realms: routes.append("LogosHistorian")
    if 'vindicta-economy' in active_realms: routes.append("VoidBanker")
    
    # If no tasks to route, end execution
    if not routes:
        logger.info("no_tasks_to_route")
        return END
    
    logger.info("routing_tasks", target_nodes=routes)
    return routes

def build_domain_graph():
    # Build the Domain-Graph
    domain_builder = StateGraph(VindictaState)
    domain_builder.add_node("SetupExecution", setup_execution_node)
    domain_builder.add_node("TechPriest", tech_priest_node)
    domain_builder.add_node("LogosHistorian", logos_historian_node)
    domain_builder.add_node("VoidBanker", void_banker_node)

    domain_builder.add_edge("TechPriest", END)
    domain_builder.add_edge("LogosHistorian", END)
    domain_builder.add_edge("VoidBanker", END)

    # Conditional routing allows parallel execution based on task realms
    domain_builder.set_entry_point("SetupExecution")
    domain_builder.add_conditional_edges(
        "SetupExecution",
        task_router,
        {
            "TechPriest": "TechPriest",
            "LogosHistorian": "LogosHistorian",
            "VoidBanker": "VoidBanker",
            END: END
        }
    )

    return domain_builder.compile()

# Export instance
domain_graph = build_domain_graph()
