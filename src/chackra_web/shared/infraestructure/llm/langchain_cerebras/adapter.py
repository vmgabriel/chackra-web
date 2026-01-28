from typing import Type, Any
import re
import json
import pydantic
import langchain_cerebras

from langchain_core import prompts
from langchain_core.output_parsers import BaseOutputParser

from chackra_web.shared.domain.model.configuration import configuration as shared_configration
from chackra_web.shared.domain.model.logger import logger as shared_logger
from chackra_web.shared.domain.model.llm import base as shared_llm



class CleanJsonOutputParser(BaseOutputParser):
    pydantic_object: Type[pydantic.BaseModel]

    def parse(self, text: str) -> Any:
        cleaned = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
        match = re.search(r"\{.*\}", cleaned, re.DOTALL)
        if not match:
            raise ValueError(f"No se encontró JSON en la respuesta: {text[:200]}...")
        json_str = match.group()
        try:
            data = json.loads(json_str)
            return self.pydantic_object(**data)
        except json.JSONDecodeError as e:
            raise ValueError(f"JSON inválido: {e}")

    def get_format_instructions(self) -> str:
        return "Responde exclusivamente con un objeto JSON válido."


class CerebrasGenericAdapter(shared_llm.GenericLLMPort):
    def __init__(
        self,
        configuration: shared_configration.Configuration,
        logger: shared_logger.LogAdapter,
    ):
        super().__init__(configuration=configuration, logger=logger)
        self._llm = langchain_cerebras.ChatCerebras(
            model=configuration.model_name,
            # base_url=self.configuration.cerebras_url,
            temperature=self.configuration.model_temperature,
            api_key=self.configuration.cerebras_api_key,
        )
        self.logger.info(f"Ollama LLM initialized with model: {configuration.model_name}")

    def invoke(self, messages, response_model):
        try:
            langchain_msgs = []
            for msg in messages:
                content_str = str(msg.content)
                role_map = {
                    shared_llm.MessageRole.SYSTEM: "system",
                    shared_llm.MessageRole.USER: "human",
                    shared_llm.MessageRole.ASSISTANT: "ai",
                }
                langchain_msgs.append((role_map[msg.role], content_str))

            self.logger.info(f"Invoking LLM with messages: {langchain_msgs}")

            parser = CleanJsonOutputParser(pydantic_object=response_model)
            prompt = prompts.ChatPromptTemplate.from_messages(langchain_msgs)

            chain = prompt | self._llm | parser
            response_obj = chain.invoke({})

            return shared_llm.OutputResponse(response=response_obj)

        except Exception as e:
            self.logger.error(f"Error invoking Cerebras LLM: {e}")
            return shared_llm.OutputResponse(
                errors=[str(e)],
                context=[{"input": [m.content.model_dump() for m in messages]}]
            )
