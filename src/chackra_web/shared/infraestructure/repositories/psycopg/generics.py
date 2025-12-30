from typing import Type

import psycopg

from chackra_web.shared.domain.model.behavior import behavior as shared_behavior
from chackra_web.shared.domain.model.repository import exceptions as repository_exceptions
from chackra_web.shared.domain.model.uow import uow as shared_uow
from chackra_web.shared.infraestructure.repositories.psycopg import commons as psycopg_commons

from chackra_web.shared.domain.model.pagination import pagination as shared_pagination


CREATE_GENERIC_QUERY = """
INSERT INTO {table_name}({fields})
 VALUES ({placeholder})
 RETURNING *
;
"""
FIND_BY_ID_QUERY = """
SELECT * FROM {table_name} WHERE id = %s AND active = true;
"""
MATCHING_QUERY = """
SELECT * FROM {table_name} {specificator} {paginator};
"""
MATCHING_COUNT_QUERY = """
SELECT COUNT(*) FROM {table_name} {specificator};
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
            params=(id.value,),
            uow=self.uow,
            model_class=Type[shared_behavior.M],
            serializer=self.serializer,
        )


class PsycopgGenericLister(shared_behavior.ListerBehavior[shared_behavior.M]):
    MATCHING_QUERY = """
    SELECT * FROM {table_name} {specificator} {paginator};
    """
    MATCHING_COUNT_QUERY = """
    SELECT COUNT(*) FROM {table_name} {specificator};
    """

    table_name: str
    uow: shared_uow.UOW
    serializer: psycopg_commons.SafeSerializer
    model_class: Type[shared_behavior.M]

    def __init__(
            self,
            table_name: str,
            uow: shared_uow.UOW,
            model_class: Type[shared_behavior.M],
            serializer: psycopg_commons.SafeSerializer = psycopg_commons.BasicTypeSerializer()
    ) -> None:
        self.table_name = table_name
        self.uow = uow
        self.serializer = serializer
        self.model_class = model_class

    def matching(self, pagination: shared_pagination.Pagination) -> shared_pagination.Paginator:
        filters_data: tuple = tuple()
        filters: str = ""

        if pagination.filters:
            filters, filters_data = pagination.filters.to_sql()
            filters = f"WHERE {filters}"

        order_by_conversation = [ordered.to_sql() for ordered in pagination.order_by if ordered]

        limit_sql = pagination.page_size_to_sql()
        offset_sql = pagination.page_to_sql()

        paginator = f"ORDER BY {','.join(order_by_conversation)} " if order_by_conversation else ""
        paginator += f"{limit_sql} {offset_sql}"

        count_query = self.MATCHING_COUNT_QUERY.format(table_name=self.table_name, specificator=filters)
        print("count_query - ", count_query)
        data_query = self.MATCHING_QUERY.format(table_name=self.table_name, specificator=filters, paginator=paginator)
        print("data_query - ", data_query)

        print("filters_data - ", filters_data)

        entities = []
        with self.uow.session() as session:
            try:
                count_result = session.atomic_execute(count_query, filters_data)
                count_row = count_result.fetchone()
                total = count_row[0] if count_row else 0

                print("total - ", total)
                result = session.atomic_execute(data_query, filters_data)
                rows = result.fetchall()

                column_names = [desc[0] for desc in result.description]
                for row in rows:
                    db_data = dict(zip(column_names, row))
                    db_data["id"] = {"value": db_data["id"]}
                    for k, v in db_data.items():
                        if k.endswith("_id"):
                            db_data[k] = {"value": v}

                    entities.append(self.serializer.from_primitive(db_data, self.model_class))

            except psycopg.Error as e:
                raise repository_exceptions.RepositoryError(f"Error executing query: {str(e)}")

        return shared_pagination.Paginator(
            page_size=pagination.page_size,
            page=pagination.page,
            total=total,
            entities=entities,
        )


class PsycopgGenericDeleter(shared_behavior.DeleterBehavior[shared_behavior.ID]):
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

    def delete(self, id: shared_behavior.ID) -> None:
        query = f"UPDATE {self.table_name} SET active = false WHERE id = %s;"
        with self.uow.session() as session:
            try:
                session.atomic_execute(query, (id.value,))
                session.commit()
            except psycopg.Error as e:
                raise repository_exceptions.RepositoryError(f"Error executing query: {str(e)}")
