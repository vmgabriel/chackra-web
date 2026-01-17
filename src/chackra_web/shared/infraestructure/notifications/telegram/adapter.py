from typing import Any

import requests

from chackra_web.shared.domain.model.notifications import base as shared_notifications
from chackra_web.shared.domain.model.configuration import configuration as shared_configuration
from chackra_web.shared.domain.model.logger import logger as shared_logger


class TelegramNotifier(shared_notifications.NotificationPort):
    def __init__(
            self,
            configuration: shared_configuration.Configuration,
            logger: shared_logger.LogAdapter,
    ):
        super().__init__(configuration=configuration, logger=logger)
        if not self.configuration.notification_token:
            raise ValueError("El token de Telegram no puede estar vacío")
        bot_token = self.configuration.notification_token
        self.timeout = self.configuration.notification_timeout

        self.base_url = f"https://api.telegram.org/bot{bot_token}"

    def send_message(self, recipient_id: str, message: str, metadata: dict[str, Any] | None = None) -> bool:
        if not recipient_id or not message.strip():
            self.logger.warning("Intento de enviar mensaje vacío o sin destinatario.")
            return False

        url = f"{self.base_url}/sendMessage"
        payload = {
            "chat_id": recipient_id,
            "text": message,
            "parse_mode": "HTML",
        }

        try:
            response = requests.post(url, json=payload, timeout=self.timeout)
            if response.status_code == 200:
                self.logger.info(f"Mensaje enviado a {recipient_id}")
                return True
            else:
                error_detail = response.json().get("description", "Sin detalles")
                self.logger.error(f"Error al enviar a Telegram ({recipient_id}): {error_detail}")
                return False

        except requests.exceptions.RequestException as e:
            self.logger.error(f"Excepción de red al enviar a Telegram: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Error inesperado al enviar a Telegram: {e}")
            return False
