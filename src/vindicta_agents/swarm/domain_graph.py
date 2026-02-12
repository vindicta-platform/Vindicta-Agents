"""
Domain Graph Module
===================

This module defines the Vindicta Swarm's domain graph, which orchestrates task execution across different
functional domains (realms). It constructs a state graph where each node represents a domain specialist
(e.g., TechPriest, VoidBanker) capable of performing specific tasks.

Key Components:
- **Integrity Checks**: Verifies the health and connectivity of domain repositories.
- **Domain Nodes**: Wrappers around domain-specific logic (currently just integrity checks).
- **Task Router**: Routes tasks to the appropriate domain node based on the target realm.
- **Domain Graph**: The compiled LangGraph executable.

The graph is built dynamically from the `DOMAIN_REGISTRY`, allowing for easy extension of new domains.
"""

from typing import Any, Dict, List, Optional, TypedDict, Union, Callable
import functools
import json
import os
import subprocess
import sys

from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableConfig

from .state import VindictaState
from .domain_registry import DOMAIN_REGISTRY, DomainInfo
from ..utils.logger import logger


class IntegrityCheckResult(TypedDict, total=False):
    """Result structure for an integrity check operation."""
    status: str
    error: Optional[str]
    raw_output: Optional[str]
    # Allow other keys from the JSON output
    __extra__: str


# --- Helper: Integrity Check Logic ---

def _get_platform_root() -> str:
    """
    Determines the root directory of the Vindicta Platform.
    
    Returns:
        str: Absolute path to the platform root.
    """
    platform_root = os.environ.get("VINDICTA_PLATFORM_ROOT")
    if not platform_root:
        # Fallback: assume peer directories in a flat workspace
        # (e.g. CWD is Vindicta-Agents/..., so we go up to Vindicta-Agents then up to platform root)
        # Note: Original code assumed CWD is Vindicta-Agents root.
        # If CWD is src/..., we might need to adjust.
        # Assuming execution from repo root as per standard practice.
        platform_root = os.path.abspath(os.path.join(os.getcwd(), ".."))
    return platform_root


def _get_python_check_cmd(repo_path: str, package_name: str) -> List[str]:
    """Generates the command to check integrity for a Python domain."""
    # Use sys.path.append('src') for safety across all python repos
    # We use 'python -c' to avoid needing to install the package in editable mode if not already done
    python_code = (
        f"import sys; sys.path.append('src'); "
        f"from {package_name}.integrity import verify_integrity; "
        f"import json; print(json.dumps(verify_integrity()))"
    )
    
    return [
        "uv", "run", "--project", repo_path,
        "python", "-c", python_code
    ]


def _get_node_ts_check_cmd(repo_path: str, package_name: str) -> List[str]:
    """Generates the command to check integrity for a Node.js/TypeScript domain."""
    # Execute via package script using pnpm filter if it's the UI kit
    if "ui-kit" in package_name:
         return ["pnpm", "--filter", package_name, "run", "check-integrity"]
    return ["npm", "run", "check-integrity"]


def _execute_check_cmd(cmd: List[str], cwd: str) -> IntegrityCheckResult:
    """
    Executes a subprocess command and parses the JSON output.

    Args:
        cmd: The command line arguments.
        cwd: The working directory for the command.

    Returns:
        IntegrityCheckResult: The parsed result or error information.
    """
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=True,
            shell=True if os.name == 'nt' else False # Shell=True often needed on Windows for path resolution
        )
        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError:
            return {"status": "error", "raw_output": result.stdout}
            
    except subprocess.CalledProcessError as e:
        logger.error(f"integrity_check_failed", command=cmd, error=str(e), stderr=e.stderr)
        return {"status": "check_failed", "error": e.stderr}
    except Exception as e:
        logger.error(f"integrity_check_execution_error", command=cmd, error=str(e))
        return {"status": "execution_error", "error": str(e)}


def run_integrity_check(realm: str) -> IntegrityCheckResult:
    """
    Executes the integrity check command for the given realm.

    Args:
        realm: The key of the domain in DOMAIN_REGISTRY.

    Returns:
        IntegrityCheckResult: The status of the integrity check.
    """
    domain = DOMAIN_REGISTRY.get(realm)
    if not domain:
        return {"status": "error", "error": f"Realm {realm} not found in registry"}

    platform_root = _get_platform_root()
    repo_path = os.path.join(platform_root, domain['repo_name'])

    # Safety check
    if not os.path.isdir(repo_path):
         return {
             "status": "error",
             "error": f"Repository path not found: {repo_path}. Set VINDICTA_PLATFORM_ROOT if layout differs."
         }

    package_name = domain.get("package_name", "")
    primary_language = domain.get("primary_language", "").lower()
    tech_stack = domain.get("tech_stack", "").lower()

    cmd: List[str] = []
    
    if "python" in primary_language:
        cmd = _get_python_check_cmd(repo_path, package_name)
    elif "javascript" in primary_language or "node" in tech_stack:
        cmd = _get_node_ts_check_cmd(repo_path, package_name)
    else:
        return {"status": "unknown_tech_stack", "error": f"Unknown stack for {realm}"}

    return _execute_check_cmd(cmd, cwd=repo_path)


# --- Generic Node Factory ---

def make_domain_node(realm: str) -> Callable[[VindictaState, RunnableConfig], Dict[str, Any]]:
    """
    Creates a LangGraph node function for a specific domain.

    Args:
        realm: The registered domain key (e.g., 'vindicta-engine').

    Returns:
        Callable: A function matching the Node signature (state, config) -> dict.
    """
    domain = DOMAIN_REGISTRY.get(realm)
    node_name = domain["node_name"] if domain else "UnknownNode"

    def domain_node(state: VindictaState, config: RunnableConfig) -> Dict[str, Any]:
        logger.info(f"{node_name.lower()}_activated", realm=realm)
        status = run_integrity_check(realm)
        log_entry = f"{node_name}: {status.get('status', 'unknown')} - {status}"
        return {"execution_log": [log_entry]}
    
    # Set metadata for better debugging/visualization
    domain_node.__name__ = f"{node_name.lower()}_node"
    return domain_node


def setup_execution_node(state: VindictaState) -> Dict[str, Any]:
    """Initializes the execution phase."""
    logger.info("execution_phase_initializing")
    return {"current_phase": "execution"}


# --- The Router ---

def task_router(state: VindictaState) -> Union[List[str], str]:
    """
    Routes tasks to the appropriate domain nodes based on pending tasks.

    Args:
        state: The current VindictaState.

    Returns:
        Union[List[str], str]: A list of node names to execute in parallel, or END.
    """
    tasks = state.get("tasks", [])
    active_realms = set(
        t["target_realm"] for t in tasks if t.get("status") == "pending"
    )

    routes = []
    # Iterate through registry to match realms to node names
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
    """
    Constructs and compiles the StateGraph for the domain layer.

    Returns:
        CompiledStateGraph: The executable LangGraph.
    """
    domain_builder = StateGraph(VindictaState)
    
    # 1. Add Setup Node
    domain_builder.add_node("SetupExecution", setup_execution_node)
    
    # 2. Add Domain Nodes Dynamically
    node_names = []
    for realm, info in DOMAIN_REGISTRY.items():
        node_name = info["node_name"]
        node_func = make_domain_node(realm)
        domain_builder.add_node(node_name, node_func)
        node_names.append(node_name)

    # 3. Define Conditional Edges Logic
    # The router returns a list of node names. We map each possible node name to itself.
    route_map = {name: name for name in node_names}
    route_map[END] = END

    # 4. Add Edges to END
    # After a domain node runs, it goes to END (for this sub-graph execution)
    for node_name in node_names:
        domain_builder.add_edge(node_name, END)

    # 5. Set Entry Point and Routing
    domain_builder.set_entry_point("SetupExecution")
    domain_builder.add_conditional_edges(
        "SetupExecution",
        task_router,
        route_map
    )

    return domain_builder.compile()


# Export instance
domain_graph = build_domain_graph()
