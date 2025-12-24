from typing import Type

import psycopg

from chackra_web.shared.domain.model.behavior import behavior as shared_behavior
from chackra_web.shared.domain.model.repository import exceptions as repository_exceptions
from chackra_web.shared.domain.model.uow import uow as shared_uow
from chackra_web.shared.infraestructure.repositories.psycopg import commons as psycopg_commons


CREATE_GENERIC_QUERY = """
INSERT INTO {table_name}({fields})
 VALUES ({placeholder})
 RETURNING *
;
"""
FIND_BY_ID_QUERY = """
SELECT * FROM {table_name} WHERE id = %s; AND enabled = false;
"""


class PsycopgGenericCreator(shared_behavior.CreatorBehavior[shared_behavior.M]):
    table_name: str
    uow: shared_uow.UOW
    serializer: psycopg_commons.SafeSerializer

    def __init__(
            self,
            table_name: str,
            uow: shared_uow.UOW,
            serializer: psycopg_commons.SafeSerializer = psycopg_commons.BasicTypeSerializer()
    ) -> None:
        self.table_name = table_name
        self.uow = uow
        self.serializer = serializer

    def create(self, entity: shared_behavior.M) -> shared_behavior.M:
        try:
            entity_data = entity.model_dump(exclude_none=True, exclude=("id",))
            entity_data["id"] = entity.id.value
            for k, v in entity_data.items():
                if k.endswith("_id") and isinstance(v, dict) and "value" in v:
                    entity_data[k] = v["value"]
            safe_data = self.serializer.to_primitive(entity_data)
        except ValueError as e:
            raise ValueError(f"Cannot safely serialize entity: {e}")

        fields = list(safe_data.keys())
        values = list(safe_data.values())
        placeholders = ["%s" for _ in fields]

        query = CREATE_GENERIC_QUERY.format(
            table_name=self.table_name,
            fields=", ".join(fields),
            placeholder=", ".join(placeholders)
        )

        with self.uow.session() as session:
            try:
                result = session.atomic_execute(query, values)
                row = result.fetchone()

                column_names = [desc[0] for desc in result.description]
                db_data = dict(zip(column_names, row))
                db_data["id"] = {"value": db_data["id"]}
                for k, v in db_data.items():
                    if k.endswith("_id"):
                        db_data[k] = {"value": v}

                session.commit()
                return self.serializer.from_primitive(db_data, entity.__class__)

            except psycopg.Error as e:
                raise repository_exceptions.RepositoryError(f"Error creating entity: {str(e)}")


class PsycopgGenericFinder(shared_behavior.FinderBehavior[shared_behavior.M, shared_behavior.ID]):
    table_name: str
    uow: shared_uow.UOW
    serializer: psycopg_commons.SafeSerializer

    def __init__(
            self,
            table_name: str,
            uow: shared_uow.UOW,
            serializer: psycopg_commons.SafeSerializer = psycopg_commons.BasicTypeSerializer()
    ) -> None:
        self.table_name = table_name
        self.uow = uow
        self.serializer = serializer


    def find_by_id(self, id: shared_behavior.ID) -> shared_behavior.M | None:
        query = FIND_BY_ID_QUERY.format(table_name=self.table_name)
        return psycopg_commons.execute_query(
            query=query,
            params=(id,),
            uow=self.uow,
            model_class=Type[shared_behavior.M],
            serializer=self.serializer,
        )
