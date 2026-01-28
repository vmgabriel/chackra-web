import langchain_ollama

from langchain_core import prompts, output_parsers

from chackra_web.shared.domain.model.configuration import configuration as shared_configration
from chackra_web.shared.domain.model.logger import logger as shared_logger
from chackra_web.shared.domain.model.llm import base as shared_llm


class OllamaGenericAdapter(shared_llm.GenericLLMPort):
    def __init__(
        self,
        configuration: shared_configration.Configuration,
        logger: shared_logger.LogAdapter,
    ):
        super().__init__(configuration=configuration, logger=logger)
        self._llm = langchain_ollama.ChatOllama(
            model=configuration.model_name,
            base_url=self.configuration.ollama_url,
            temperature=self.configuration.model_temperature,
            format="json",
        )
        self.logger.info(f"Ollama LLM initialized with model: {configuration.model_name}")
        self.logger.info(f"Ollama LLM base URL: {self.configuration.ollama_url}")

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

            parser = output_parsers.JsonOutputParser(pydantic_object=response_model)
            prompt = prompts.ChatPromptTemplate.from_messages(langchain_msgs)

            chain = prompt | self._llm | parser
            self.logger.info(f"Chain {chain}")
            result_dict = chain.invoke({})
            self.logger.info(f"Result dict: {result_dict}")

            response_obj = response_model(**result_dict)
            return shared_llm.OutputResponse(response=response_obj)

        except Exception as e:
            return shared_llm.OutputResponse(
                errors=[str(e)],
                context=[{"input": [m.content.model_dump() for m in messages]}]
            )
