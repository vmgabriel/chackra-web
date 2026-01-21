from typing import Any
from chackra_web.shared.infraestructure.repositories.psycopg import commons as psycopg_commons

TABLE_NAME: str = "tbl_user"
ADDITIONAL_TABLE_NAME: str = "tbl_additional_information_user"


class AdditionalInformationUserSerializer(psycopg_commons.BasicTypeSerializer):
    def from_primitive(self, value: Any, model_class: type[psycopg_commons.T]) -> psycopg_commons.T | None:
        if value is None:
            return None
        if isinstance(value, dict):
            value["foods"] = value["foods"].split(",")
            return model_class(**value)
        raise ValueError(f"Cannot convert {type(value)} to {model_class}")
