from typing import Type

import psycopg

from chackra_web.shared.domain.model.uow import uow as shared_uow
from chackra_web.shared.infraestructure.repositories.psycopg import commons as psycopg_commons
from chackra_web.shared.domain.model.behavior import behavior as shared_behavior
from chackra_web.auth.domain.models import behavior as auth_behavior
from chackra_web.shared.domain.model.auth import enums as auth_enums
from chackra_web.auth.domain.models import auth as domain_auth
from chackra_web.shared.domain.model.auth import auth_id as domain_auth_id
from chackra_web.auth.infraestructure.repositories.psycopg import commons as psycopg_auth_commons
from chackra_web.shared.domain.model.repository import exceptions as repository_exceptions


class PsycopgAuthBaseUpdaterRepository(
    shared_behavior.UpdaterBehavior[shared_behavior.M, shared_behavior.ID],
    auth_behavior.ChangeRoleBehavior[shared_behavior.M]
):
    table_name: str
    uow: shared_uow.UOW
    serializer: psycopg_commons.SafeSerializer = psycopg_commons.BasicTypeSerializer()
    model_class: Type[shared_behavior.M]

    def __init__(
            self,
            table_name: str,
            uow: shared_uow.UOW,
            model_class: Type[shared_behavior.M],
            serializer: psycopg_commons.SafeSerializer = psycopg_commons.BasicTypeSerializer(),
    ) -> None:
        super().__init__(uow)
        self.table_name = table_name
        self.uow = uow
        self.serializer = serializer
        self.model_class = model_class

    def change_role(self, id: shared_behavior.ID, role: auth_enums.AuthRole) -> None:
        query = f"UPDATE {self.table_name} SET auth_role = %s WHERE id = %s AND active = true;"
        with self.uow.session() as session:
            session.atomic_execute(query, (role.value, id.value))
            session.commit()

        return None

    def update(self, id: shared_behavior.ID, entity: shared_behavior.M) -> shared_behavior.M:
        UPDATE_GENERIC_QUERY = "UPDATE {table_name} SET {placeholder} WHERE id = %s AND active = true;"

        try:
            entity_data = entity.model_dump(exclude_none=True, exclude=("id",))
            entity_data["id"] = entity.id.value
            for k, v in entity_data.items():
                if k.endswith("_id") and isinstance(v, dict) and "value" in v:
                    entity_data[k] = v["value"]
            safe_data = self.serializer.to_primitive(entity_data)
        except ValueError as e:
            raise ValueError(f"Cannot safely serialize entity: {e}")

        placeholders = [f"{field} = %s" for field in safe_data.key()]
        values = tuple(safe_data.values()) + (id.value,)

        query = UPDATE_GENERIC_QUERY.format(
            table_name=self.table_name,
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


class PsycopgAuthUpdaterRepository(PsycopgAuthBaseUpdaterRepository[domain_auth.AuthUser, domain_auth_id.AuthId]):
    def __init__(self, uow: shared_uow.UOW) -> None:
        super().__init__(
            table_name=psycopg_auth_commons.TABLE_NAME,
            uow=uow,
            model_class=domain_auth.AuthUser,
            serializer=psycopg_commons.BasicTypeSerializer()
        )
