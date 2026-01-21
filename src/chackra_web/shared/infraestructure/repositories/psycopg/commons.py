from typing import TypeVar, Protocol, Any, Type

import enum
import pydantic
import dataclasses
import datetime
import uuid
import decimal

import psycopg

from chackra_web.shared.domain.model.id import model as id_model
from chackra_web.shared.domain.model.uow import uow as shared_uow
from chackra_web.shared.domain.model.repository import exceptions as repository_exceptions


T = TypeVar('T', bound=pydantic.BaseModel)


class SafeSerializer(Protocol):
    def to_primitive(self, value: Any) -> Any: ...
    def from_primitive(self, value: Any, model_class: type[T]) -> T | None: ...


@dataclasses.dataclass
class BasicTypeSerializer(SafeSerializer):
    SAFE_TYPES = (
        str, int, float,
        bool, type(None), datetime.datetime,
        decimal.Decimal, uuid.UUID, id_model.BaseId,
        pydantic.BaseModel, enum.Enum
    )
    EXTENDED_SAFE_TYPES = (
        dict, list, datetime.time, datetime.date
    )

    def _is_safe_dict(self, value: dict) -> bool:
        return all(
            isinstance(k, str) and
            isinstance(v, self.SAFE_TYPES + self.EXTENDED_SAFE_TYPES)
            for k, v in value.items()
        )

    def _is_safe_list(self, value: list) -> bool:
        return all(
            isinstance(v, self.SAFE_TYPES + self.EXTENDED_SAFE_TYPES)
            for v in value
        )

    def to_primitive(self, value: Any) -> Any:
        if isinstance(value, self.SAFE_TYPES):
            return value
        elif isinstance(value, dict):
            if not self._is_safe_dict(value):
                raise ValueError("Dict contains unsafe types")
            return {k: self.to_primitive(v) for k, v in value.items()}
        elif isinstance(value, list):
            if not self._is_safe_list(value):
                raise ValueError("List contains unsafe types")
            return [self.to_primitive(v) for v in value]
        elif isinstance(value, enum.Enum):
            return value.value
        elif isinstance(value, datetime.datetime):
            return value.isoformat()
        elif isinstance(value, datetime.date):
            return value.strftime("%Y-%m-%d")
        elif isinstance(value, datetime.time):
            return value.strftime("%H:%M")
        elif isinstance(value, uuid.UUID):
            return str(value)
        elif isinstance(value, decimal.Decimal):
            return str(value)
        elif isinstance(value, id_model.BaseId):
            return str(value)
        elif isinstance(value, pydantic.BaseModel):
            return self.to_primitive(value.model_dump(exclude_none=True))
        raise ValueError(f"Unsafe type: {type(value)}")

    def from_primitive(self, value: Any, model_class: type[T]) -> T | None:
        if value is None:
            return None
        if isinstance(value, dict):
            return model_class(**value)
        raise ValueError(f"Cannot convert {type(value)} to {model_class}")


def execute_query(
        query: str,
        params: tuple,
        uow: shared_uow.UOW,
        model_class: Type[T],
        serializer: SafeSerializer
) -> T | None:
    with uow.session() as session:
        try:
            result = session.atomic_execute(query, params)
            row = result.fetchone()

            if not row:
                return None

            column_names = [desc[0] for desc in result.description]
            db_data = dict(zip(column_names, row))
            db_data["id"] = {"value": db_data["id"]}
            for k, v in db_data.items():
                if k.endswith("_id"):
                    db_data[k] = {"value": v}

            return serializer.from_primitive(db_data, model_class)

        except psycopg.Error as e:
            raise repository_exceptions.RepositoryError(
                f"Error executing query: {str(e)}"
            )
