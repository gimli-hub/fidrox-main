from typing import Any

from fidroxai_core.graph.models import create_structured_output_model, get_model
from fidroxai_core.plugins.utilities.base import BaseUtility
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field



class LLMUtility(BaseUtility):
    llm_job_description: str = Field(
        description="Explicit description of the llm what it should do."
    )
    structured_output: type[BaseModel] | None = None
    fields_to_retain: list[str] = []
    model_name: str = "gpt-4o"

    async def arun(self, *args, **kwargs) -> BaseModel | dict | str | Any:
        placeholders = await self._arun(*args, **kwargs)

        if isinstance(placeholders, str):
            return placeholders

        prompt = PromptTemplate.from_template(self.llm_job_description)
        llm = get_model(self.model_name)

        if self.structured_output is not None:
            llm = create_structured_output_model(self.structured_output, llm)
            chain = prompt | llm
        else:
            chain = prompt | llm | StrOutputParser()

        llm_result = await chain.ainvoke(placeholders)

        result = {
            "result": llm_result
        }
        if self.fields_to_retain:
            result = {
                **{field: placeholders[field] for field in self.fields_to_retain},
                **result,
            }
        return result
