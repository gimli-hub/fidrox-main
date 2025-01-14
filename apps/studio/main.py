from fidroxai_core.graph.models import get_model
from langgraph.checkpoint.sqlite import SqliteSaver

from fidroxai_core.graph import create_graph
from fidroxai_core.plugins.registry import ensure_plugin_registry
from apps.fidrox_brain import _preload_modules
from settings import settings


def test_chat():
    _preload_modules()
    plugin_names = [
        "wallet",
        "fidrox",
        "coin-technical-analyzer",
        "coin-technical-chart-searcher",
    ]
    registry = ensure_plugin_registry()
    plugins = [registry.plugins[plugin_name]() for plugin_name in plugin_names]
    plugins = [p for p in plugins if p.exclude is False]

    llm = get_model()

    with SqliteSaver.from_conn_string(":memory:") as saver:
        graph = create_graph(llm, plugins, memory=saver)

    return graph
