from libs.community.plugins.fidrox.tools import TOOLS
from fidroxai_core.plugins import BasePlugin
from fidroxai_core.plugins.registry import ensure_plugin_registry
from fidroxai_core.plugins.tools import BaseTool

plugin_registry = ensure_plugin_registry()


@plugin_registry.register("off-topic")
class OffTopicPlugin(BasePlugin):
    name: str = "off-topic"
    description: str = "Agent for responding to off-topic requests, which are not related to FidroxAI plugins."
    tools: list[BaseTool] = TOOLS
