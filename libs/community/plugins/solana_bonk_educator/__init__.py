from libs.community.plugins.solana_bonk_educator.tools import TOOLS
from fidroxai_core.plugins import BasePlugin
from fidroxai_core.plugins.registry import ensure_plugin_registry
from fidroxai_core.plugins.tools import BaseTool

plugin_registry = ensure_plugin_registry()


@plugin_registry.register("solana-bonk-educator")
class SolanaBonkEducatorPlugin(BasePlugin):
    name: str = "Solana Bonk Educator"
    description: str = "Bonk-Enriched Plugin, answers questions on crypto, blockchain operations, solana, bonk and more."
    owner: str = "2snYEzbMckwnv85MW3s2sCaEQ1wtKZv2cj9WhbmDuuRD"
    tools: list[BaseTool] = TOOLS
    image_url: str = "https://fidrox-ai-assets.s3.eu-central-1.amazonaws.com/agent-avatars/solana-bonk-educator.png"
