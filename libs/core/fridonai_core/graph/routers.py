from langgraph.graph import END
from langgraph.prebuilt import tools_condition

from fidroxai_core.graph.states import State
from fidroxai_core.graph.tools import CompleteTool


def route_plugin_agent(
    state,
) -> str:
    route = tools_condition(state)
    if route == END:
        return END
    tool_calls = state["messages"][-1].tool_calls
    did_cancel = any(tc["name"] == CompleteTool.__name__ for tc in tool_calls)
    if did_cancel:
        return END
    return "tool_node"


def route_supervisor_agent(state: State, wrapped_plugins_to_plugins) -> str:
    tool_calls = state["messages"][-1].tool_calls
    if not tool_calls:
        return "respond"
    return wrapped_plugins_to_plugins[tool_calls[0]["name"]]