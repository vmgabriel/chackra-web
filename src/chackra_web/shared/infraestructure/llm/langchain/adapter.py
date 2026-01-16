import langchain_ollama

from langchain_core import prompts, output_parsers

from chackra_web.shared.domain.model.configuration import configuration as shared_configration
from chackra_web.shared.domain.model.llm import base as shared_llm


class OllamaGenericAdapter(shared_llm.GenericLLMPort):
    def __init__(
        self,
        configuration: shared_configration.Configuration,
    ):
        super().__init__(configuration=configuration)
        self._llm = langchain_ollama.ChatOllama(
            model=configuration.model_name,
            base_url=self.configuration.ollama_url,
            temperature=self.configuration.model_temperature,
            format="json",
        )

    def invoke(self, messages, response_model):
        try:
            langchain_msgs = []
            for msg in messages:
                content_str = msg.content.model_dump_json()
                role_map = {
                    shared_llm.MessageRole.SYSTEM: "system",
                    shared_llm.MessageRole.USER: "human",
                    shared_llm.MessageRole.ASSISTANT: "ai",
                }
                langchain_msgs.append((role_map[msg.role], content_str))

            parser = output_parsers.JsonOutputParser(pydantic_object=response_model)
            prompt = prompts.ChatPromptTemplate.from_messages(langchain_msgs)

            chain = prompt | self._llm | parser
            result_dict = chain.invoke({})

            response_obj = response_model(**result_dict)
            return output_parsers.OutputResponse(response=response_obj)

        except Exception as e:
            return output_parsers.OutputResponse(
                errors=[str(e)],
                context=[{"input": [m.content.model_dump() for m in messages]}]
            )
