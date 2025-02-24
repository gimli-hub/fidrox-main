import os
from typing import Literal
from fidroxai_core.graph.models import get_model
from langchain_core.language_models import BaseChatModel
from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.graph import END, StateGraph
from langchain_core.messages import HumanMessage

from fidroxai_core.graph.agents import create_agent
from fidroxai_core.graph.prompts import create_agent_prompt, create_supervised_prompt
from fidroxai_core.graph.routers import route_supervisor_agent
from fidroxai_core.graph.states import State, attach_tool_response_to_tool
from fidroxai_core.graph.tools import CompleteTool, create_plugin_wrapper_tool
from fidroxai_core.graph.utils import (
    generate_structured_response,
    prepare_plugin_agent,
)
from fidroxai_core.plugins import BasePlugin


def create_graph(
    llm: BaseChatModel, plugins: list[BasePlugin], memory: BaseCheckpointSaver
):
    plugins_to_wrapped_plugins = {
        p.name: create_plugin_wrapper_tool(p, type(p).__name__) for p in plugins
    }
    wrapped_plugins_to_plugins = {
        wp.__name__: pname for pname, wp in plugins_to_wrapped_plugins.items()
    }

    workflow = StateGraph(State)

    supervisor_agent = create_agent(
        create_supervised_prompt(),
        [*list(plugins_to_wrapped_plugins.values())],
        llm=llm,
        always_tool_call=False,
    )

    workflow.add_node("supervisor", supervisor_agent)

    for plugin in plugins:
        plugin_prompt = create_agent_prompt(
            plugin.name,
            plugin.description,
            plugin.output_format,
        )

        agent_graph = create_agent(
            plugin_prompt,
            plugin.tools_with_examples_in_description + [CompleteTool],
            always_tool_call=True,
            name=plugin.slug,
            llm=llm,
        )

        workflow.add_node(
            plugin.name,
            prepare_plugin_agent | agent_graph | attach_tool_response_to_tool,
        )
        workflow.add_edge(plugin.name, "supervisor")

    def _route_supervisor_agent_wrapper(state):
        return route_supervisor_agent(state, wrapped_plugins_to_plugins)

    workflow.add_conditional_edges(
        "supervisor",
        _route_supervisor_agent_wrapper,
        {
            **{plugin.name: plugin.name for plugin in plugins},
            "respond": "respond",
        },
    )
    workflow.add_node("respond", generate_structured_response)
    workflow.add_edge("respond", END)

    workflow.set_entry_point("supervisor")

    return workflow.compile(checkpointer=memory)


async def generate_response(
    message: str,
    plugins: list[BasePlugin],
    config: dict,
    memory: Literal["postgres"] = "postgres",
    return_used_agents: bool = True,
    llm: BaseChatModel = get_model("gpt-4o"),
):

    if memory not in ['postgres', 'sqlite']:
        raise ValueError('Only postgres and sqlite are supported for now')

    if memory == 'sqlite':
        from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver as Saver
        conn_string = ":memory:"
    else:
        from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver as Saver
        conn_string = os.environ.get("POSTGRES_DB_URL")

    async with Saver.from_conn_string(conn_string) as memory_saver:
        if memory == 'postgres':
            await memory_saver.setup()

        graph = create_graph(llm, plugins, memory_saver)
        graph_config = {"configurable": config}
        async for s in graph.astream(
            {
                "messages": [HumanMessage(content=message)],
            },
            graph_config,
            stream_mode="values",
        ):
            if "__end__" not in s:
                response = s["messages"][-1]
                response.pretty_print()

        graph_state = await graph.aget_state(graph_config)
        final_response = graph_state.values.get("final_response")
        if return_used_agents:
            used_agents = list(set(graph_state.values.get("used_agents", [])))
            return final_response, used_agents
        return final_response
