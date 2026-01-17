from chackra_web.shared.domain.model.configuration import configuration as shared_configuration
from chackra_web.shared.domain.model.logger import logger as shared_logger

from chackra_web.shared.domain.model.notifications import base as shared_notification

from chackra_web.shared.infraestructure.notifications.telegram import adapter as telegram_adapter


def get_notification_adapter(
        configuration: shared_configuration.Configuration,
        logger: shared_logger.LogAdapter
) -> shared_notification.NotificationPort:
    if configuration.notification_adapter == "telegram":
        return telegram_adapter.TelegramNotifier(configuration=configuration, logger=logger)
    raise NotImplementedError()
