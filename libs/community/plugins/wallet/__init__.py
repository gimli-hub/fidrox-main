from fidroxai_core.plugins.tools import BaseTool
from libs.community.plugins.wallet.tools import TOOLS
from fidroxai_core.plugins import BasePlugin
from fidroxai_core.plugins.registry import ensure_plugin_registry

plugin_registry = ensure_plugin_registry()


@plugin_registry.register(name="wallet")
class WalletPlugin(BasePlugin):
    name: str = "Wallet"
    description: str = "Plugin with wallet related operations, get balances, send tokens, etc."
    tools: list[BaseTool] = TOOLS
    image_url: str = "https://fidrox-ai-assets.s3.eu-central-1.amazonaws.com/agent-avatars/wallet-avatar.png"
