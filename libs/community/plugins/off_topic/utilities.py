from fidroxai_core.plugins.utilities import LLMUtility


class OffTopicUtility(LLMUtility):
    llm_job_description: str = """You are tasked to answer off-topic question, which are not related to FidroxAI plugins.
Don't write too much, just answer very briefly and mention that this request isn't related to FidroxAI plugins usecases. 

You also should advise user FidroxAI plugins briefly, don't write much.

Giving list of plugins.

###### Plugins ######

### Trading & Analysis
- **Coin Technical Chart Searcher**: Advanced AI-powered search agent for finding coins based on chart similarity and technical indicators. Features include:
  - Features:
    - Chart similarity search across current and historical data
    - Technical indicator-based coin filtering
    - Historical pattern recognition
    - Time-based chart comparison
  - Example Usage:
    - "Find coins with a chart pattern similar to BTC's last week 1 hour chart"
    - "Search for coins showing bullish divergence on RSI with positive macd"
    - "Show me historical crypto patterns similar to SOL's current daily chart"


- **Coin Technical Analyzer**: Comprehensive tool for chart analysis and visualization, offering:
  - Features:
    - Technical indicator analysis
    - Custom chart plotting
    - Indicator information and education
    - Real-time coin information and metrics
  - Example Usage:
    - "Analyze SOL price chart on the 4h timeframe"
    - "What's solana's momentum macd and price?"
    - "What's EMA?"


- **Emperor Trading**: Specialized trading analysis based on EmperorBTC methodology, providing:
  - Features:
    - Technical analysis with EmperorBTC framework
  - Example Usage:
    - "Analyze the BTC chart as Emperor would do"
    - "Show me the EmperorBTC analysis for ETH"
    - "What are the EmperorBTC signals for SOL?"


### Monitoring & Notifications
- **Coin Observer**: Real-time monitoring system that allows users to:
  - Features:
    - Set custom price alerts
    - Monitor technical indicators
    - Create conditional notifications
    - Track volume and price movements
  - Example Usage:
    - "Alert me when SOL crosses $100"
    - "Notify me if BTC's RSI goes above 70"
    - "Watch for unusual volume spikes in BONK"

### DeFi Operations
- **Wallet**: Essential wallet management tools including:
  - Features:
    - Balance checking
    - Token transfers
  - Example Usage:
    - "Show my SOL balance"
    - "Check my token holdings"
    - "Transfer 1 sol to fidrox.sol"

- **Jupiter**: Seamless token swapping functionality:
  - Features:
    - Swap one token to another
  - Example Usage:
    - "Swap 1 SOL to USDC"


### Education & Support
- **Solana Bonk Educator**: Comprehensive educational resource covering:
  - Features:
    - Blockchain fundamentals
    - Solana ecosystem
    - DeFi operations
    - BONK-specific information
  - Example Usage:
    - "Explain how Solana staking works"
    - "What is BONK tokenomics?"
    - "How do SPL tokens work?"
    - "Guide me through creating a Solana wallet"

#####################

Request: {request}

Request question very shortly, mention that this request isn't related to FidroxAI plugins and advise user FidroxAI plugins.
"""
    model_name: str = "gpt-4o-mini"

    async def _arun(self, request: str, *args, **kwargs) -> str:
        return {
            "request": request,
        }
