from chackra_web.shared.domain.model.configuration import configuration as shared_configuration
from chackra_web.shared.domain.model.logger import logger as shared_logger
from chackra_web.shared.domain.model.llm import base as shared_base

from chackra_web.shared.infraestructure.llm.langchain_ollama import adapter as langchain_adapter
from chackra_web.shared.infraestructure.llm.langchain_cerebras import adapter as langchain_cerebras_adapter


def get_llm_adapter(
        configuration: shared_configuration.Configuration,
        logger: shared_logger.LogAdapter
) -> shared_base.GenericLLMPort:
    if configuration.llm_adapter == "ollama":
        return langchain_adapter.OllamaGenericAdapter(configuration=configuration, logger=logger)
    if configuration.llm_adapter == "cerebras":
        return langchain_cerebras_adapter.CerebrasGenericAdapter(configuration=configuration, logger=logger)
    raise NotImplementedError()
