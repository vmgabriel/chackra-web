from chackra_web.shared.domain.model.configuration import configuration as shared_configuration
from chackra_web.shared.domain.model.llm import base as shared_base

from chackra_web.shared.infraestructure.llm.langchain import adapter as langchain_adapter


def get_llm_adapter(configuration: shared_configuration.Configuration) -> shared_base.GenericLLMPort:
    if configuration.llm_adapter == "ollama":
        return langchain_adapter.OllamaGenericAdapter(configuration=configuration)
    raise NotImplementedError()
