from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableConfig
from .state import VindictaState
from ..utils.logger import logger
import uuid


def setup_execution_node(state: VindictaState):
    logger.info("execution_phase_initializing")
    return {"current_phase": "execution"}


# --- Domain Node Implementations ---
def tech_priest_node(state: VindictaState, config: RunnableConfig):
    configurable = config.get("configurable", {})
    supervisor = configurable.get("supervisor")

    logger.info("tech_priest_activated", realm="vindicta-engine")
    delta = {"execution_log": ["TechPriest activated"]}

    if supervisor:
        trace_id = str(uuid.uuid4())
        supervisor.verify_state_transition(trace_id, delta)

    return delta


def logos_historian_node(state: VindictaState, config: RunnableConfig):
    configurable = config.get("configurable", {})
    supervisor = configurable.get("supervisor")

    logger.info("logos_historian_activated", realm="warscribe-system")
    delta = {"execution_log": ["LogosHistorian activated"]}

    if supervisor:
        trace_id = str(uuid.uuid4())
        supervisor.verify_state_transition(trace_id, delta)

    return delta


def void_banker_node(state: VindictaState, config: RunnableConfig):
    configurable = config.get("configurable", {})
    supervisor = configurable.get("supervisor")

    logger.info("void_banker_activated", realm="vindicta-economy")
    delta = {"execution_log": ["VoidBanker activated"]}

    if supervisor:
        trace_id = str(uuid.uuid4())
        supervisor.verify_state_transition(trace_id, delta)

    return delta


# --- The Router ---
def task_router(state: VindictaState):
    tasks = state.get("tasks", [])
    active_realms = set(
        t["target_realm"] for t in tasks if t.get("status") == "pending"
    )

    routes = []
    if "vindicta-engine" in active_realms:
        routes.append("TechPriest")
    if "warscribe-system" in active_realms:
        routes.append("LogosHistorian")
    if "vindicta-economy" in active_realms:
        routes.append("VoidBanker")

    if not routes:
        logger.info("no_tasks_to_route")
        return END

    logger.info("routing_tasks", target_nodes=routes)
    return routes


def build_domain_graph():
    domain_builder = StateGraph(VindictaState)
    domain_builder.add_node("SetupExecution", setup_execution_node)
    domain_builder.add_node("TechPriest", tech_priest_node)
    domain_builder.add_node("LogosHistorian", logos_historian_node)
    domain_builder.add_node("VoidBanker", void_banker_node)

    domain_builder.add_edge("TechPriest", END)
    domain_builder.add_edge("LogosHistorian", END)
    domain_builder.add_edge("VoidBanker", END)

    domain_builder.set_entry_point("SetupExecution")
    domain_builder.add_conditional_edges(
        "SetupExecution",
        task_router,
        {
            "TechPriest": "TechPriest",
            "LogosHistorian": "LogosHistorian",
            "VoidBanker": "VoidBanker",
            END: END,
        },
    )

    return domain_builder.compile()


# Export instance
domain_graph = build_domain_graph()
