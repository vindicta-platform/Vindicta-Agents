"""
Domain Graph Module
===================

This module defines the Vindicta Swarm's domain graph, which orchestrates task execution across functional realms.
It uses a generic node factory and a centralized domain registry persisted in JSON.

The graph supports human-in-the-loop approvals and automated integrity checks.
"""

import functools
import json
import os
import pathlib
import subprocess
import uuid
from typing import Any, Dict, List, Optional, TypedDict, Union, Callable

from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableConfig

from .state import VindictaState
from .domain_registry import DOMAIN_REGISTRY
from ..utils.logger import logger


class IntegrityCheckResult(TypedDict, total=False):
    """Result structure for an integrity check operation."""
    status: str
    error: Optional[str]
    raw_output: Optional[str]
    __extra__: str


# --- Helper: Integrity Check Logic ---

def _get_platform_root() -> str:
    platform_root = os.environ.get("VINDICTA_PLATFORM_ROOT")
    if not platform_root:
        # Fallback: assume peer directories in a flat workspace
        platform_root = os.path.abspath(os.path.join(os.getcwd(), ".."))
    return platform_root


def _get_python_check_cmd(repo_path: str, package_name: str) -> List[str]:
    python_code = (
        f"import sys; sys.path.append('src'); "
        f"from {package_name}.integrity import verify_integrity; "
        f"import json; print(json.dumps(verify_integrity()))"
    )
    return ["uv", "run", "--project", repo_path, "python", "-c", python_code]


def _get_node_ts_check_cmd(repo_path: str, package_name: str) -> List[str]:
    if "ui-kit" in package_name:
         return ["pnpm", "--filter", package_name, "run", "check-integrity"]
    return ["npm", "run", "check-integrity"]


def _execute_check_cmd(cmd: List[str], cwd: str) -> IntegrityCheckResult:
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=True,
            shell=True if os.name == 'nt' else False
        )
        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError:
            return {"status": "error", "raw_output": result.stdout}
    except subprocess.CalledProcessError as e:
        logger.error("integrity_check_failed", command=cmd, error=str(e), stderr=e.stderr)
        return {"status": "check_failed", "error": e.stderr}
    except Exception as e:
        logger.error("integrity_check_execution_error", command=cmd, error=str(e))
        return {"status": "execution_error", "error": str(e)}


def run_integrity_check(realm: str) -> IntegrityCheckResult:
    domain = DOMAIN_REGISTRY.get(realm)
    if not domain:
        return {"status": "error", "error": f"Realm {realm} not found in registry"}

    platform_root = _get_platform_root()
    repo_path = os.path.join(platform_root, domain['repo_name'])

    if not os.path.isdir(repo_path):
         return {
             "status": "error",
             "error": f"Repository path not found: {repo_path}. Set VINDICTA_PLATFORM_ROOT if layout differs."
         }

    package_name = domain.get("package_name", "")
    primary_language = domain.get("primary_language", "").lower()
    tech_stack = domain.get("tech_stack", "").lower()

    if "python" in primary_language:
        cmd = _get_python_check_cmd(repo_path, package_name)
    elif "javascript" in primary_language or "node" in tech_stack:
        cmd = _get_node_ts_check_cmd(repo_path, package_name)
    else:
        return {"status": "unknown_tech_stack", "error": f"Unknown stack for {realm}"}

    return _execute_check_cmd(cmd, cwd=repo_path)


# --- Generic Node Factory ---

def make_domain_node(realm: str) -> Callable[[VindictaState, RunnableConfig], Dict[str, Any]]:
    domain = DOMAIN_REGISTRY.get(realm)
    node_name = domain["node_name"] if domain else "UnknownNode"

    def domain_node(state: VindictaState, config: RunnableConfig) -> Dict[str, Any]:
        configurable = config.get("configurable", {})
        supervisor = configurable.get("supervisor")
        provider = configurable.get("llm_provider")  # Expecting ShowcaseProvider here if set

        logger.info(f"{node_name.lower()}_activated", realm=realm)
        
        execution_log = [f"{node_name} activated"]

        # Showcase / Auto-Execution Logic
        if provider and hasattr(provider, "execute_domain_task"):
            try:
                platform_root = _get_platform_root()
                domain_info = DOMAIN_REGISTRY.get(realm)
                if domain_info:
                    repo_path = os.path.join(platform_root, domain_info["repo_name"])
                    
                    # Execute the task via the provider's logic
                    result = provider.execute_domain_task(realm, repo_path)
                    execution_log.append(f"Task result: {result}")
            except Exception as e:
                logger.error(f"{node_name}_execution_failed", error=str(e))
                execution_log.append(f"Execution Error: {str(e)}")

        delta = {"execution_log": execution_log}
        
        if supervisor:
            trace_id = str(uuid.uuid4())
            supervisor.verify_state_transition(trace_id, delta)
            
        return delta
    
    domain_node.__name__ = f"{node_name.lower()}_node"
    return domain_node


def setup_execution_node(state: VindictaState) -> Dict[str, Any]:
    logger.info("execution_phase_initializing")
    return {"current_phase": "execution"}


# --- The Router ---

def task_router(state: VindictaState) -> Union[List[str], str]:
    tasks = state.get("tasks", [])
    active_realms = set(
        t["target_realm"] for t in tasks if t.get("status") == "pending"
    )

    routes = []
    for realm, info in DOMAIN_REGISTRY.items():
        if realm in active_realms:
            routes.append(info["node_name"])

    if not routes:
        logger.info("no_tasks_to_route")
        return END

    logger.info("routing_tasks", target_nodes=routes)
    return routes


# --- Graph Construction ---

def build_domain_graph() -> Any:
    domain_builder = StateGraph(VindictaState)
    domain_builder.add_node("SetupExecution", setup_execution_node)
    
    node_names = []
    for realm, info in DOMAIN_REGISTRY.items():
        node_name = info["node_name"]
        node_func = make_domain_node(realm)
        domain_builder.add_node(node_name, node_func)
        node_names.append(node_name)

    route_map = {name: name for name in node_names}
    route_map[END] = END

    for node_name in node_names:
        domain_builder.add_edge(node_name, END)

    domain_builder.set_entry_point("SetupExecution")
    domain_builder.add_conditional_edges("SetupExecution", task_router, route_map)

    return domain_builder.compile()


# Export instance
domain_graph = build_domain_graph()

# --- Backward Compatibility ---
tech_priest_node = make_domain_node("vindicta-engine")
logos_historian_node = make_domain_node("warscribe-system")
void_banker_node = make_domain_node("vindicta-economy")
seers_oracle_node = make_domain_node("primordia-ai")
debate_master_node = make_domain_node("meta-oracle")
forge_smith_node = make_domain_node("logi-slate-ui")
portal_archon_node = make_domain_node("vindicta-portal")
gate_knight_node = make_domain_node("vindicta-api")
