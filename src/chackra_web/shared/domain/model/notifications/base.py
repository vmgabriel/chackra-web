from typing import Any

import abc

from chackra_web.shared.domain.model.configuration import configuration as shared_configuration
from chackra_web.shared.domain.model.logger import logger as shared_logger


class NotificationPort(abc.ABC):
    """
    Generic port for sending notifications.
    """

    def __init__(
            self,
            configuration: shared_configuration.Configuration,
            logger: shared_logger.LogAdapter
    ) -> None:
        self.configuration = configuration
        self.logger = logger

    @abc.abstractmethod
    def send_message(self, recipient_id: str, message: str, metadata: dict[str, Any] | None = None) -> bool:
        """
        Abstract method for sending a message to a specified recipient. This method is intended
        to be implemented by subclasses that define specific messaging service behavior. It sends
        a message to the given recipient and optionally includes metadata about the message.

        :param recipient_id: The unique identifier of the message recipient.
        :param message: The textual content of the message to be sent.
        :param metadata: Optional dictionary containing additional information or properties
            about the message being sent. Defaults to None.
        :return: A boolean indicating the success of the message-sending operation.
        """
        raise NotImplementedError()
