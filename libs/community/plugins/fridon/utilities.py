from libs.community.helpers.chains import create_retriever_chain
from fidroxai_core.plugins.utilities import BaseUtility





class FidroxRagUtility(BaseUtility):
    async def arun(self, question: str, *args, **kwargs) -> str:
        retrieval_chain = create_retriever_chain("libs/community/plugins/fidrox/fidrox.md")
        response = await retrieval_chain.ainvoke({"input": question})

        return response
