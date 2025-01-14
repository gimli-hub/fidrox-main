from libs.community.plugins.fidrox.utilities import FidroxRagUtility
from fidroxai_core.plugins.schemas import BaseToolInput
from fidroxai_core.plugins.tools import BaseTool
from pydantic import Field


class FidroxResponderInput(BaseToolInput):
    question: str = Field(..., description="The question about FidroxAI")


FidroxResponderTool = BaseTool(
    name="fidrox-responder",
    description="Always use this tool to answer questions before CompleteTool.",
    args_schema=FidroxResponderInput,
    utility=FidroxRagUtility(),
    examples=[
        {
            "request": "What are you?",
            "response": "",
        },
        {
            "request": "What plugins do you have?",
            "response": "",
        },
        {
            "request": "Tell me about yourself",
            "response": "",
        },
        {
            "request": "What is FidroxAI's features?",
            "response": "",
        },
        {
            "request": "How can I use coin searcher plugin?",
            "response": "",
        },
    ],
)


TOOLS = [FidroxResponderTool]
