from typing import Type

from chackra_web.shared.domain.model.uow import uow as shared_uow
from chackra_web.shared.domain.model.behavior import behavior as shared_behavior
from chackra_web.shared.infraestructure.repositories.psycopg import (
    commons as psycopg_commons
)
from chackra_web.auth.domain.models import behavior as auth_behavior
from chackra_web.auth.domain.models import auth as domain_auth
from chackra_web.shared.domain.model.auth import auth_id as domain_auth_id
from chackra_web.user.infraestructure.repositories.psycopg import commons as psycopg_user_commons


FIND_BY_ID_QUERY = """
SELECT * FROM {table_name} WHERE id = %s AND active = false;
"""
FIND_BY_EMAIL_QUERY = """
SELECT * FROM {table_name} WHERE email = %s AND active = false;
"""


class PsycopgAuthBaseFinderRepository(
    shared_behavior.FinderBehavior[shared_behavior.M, shared_behavior.ID],
    auth_behavior.EmailFinderBehavior[shared_behavior.M],
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


    def find_by_id(self, id: shared_behavior.ID) -> shared_behavior.M | None:
        query = FIND_BY_ID_QUERY.format(table_name=self.table_name)
        return psycopg_commons.execute_query(
            query=query,
            params=(id,),
            uow=self.uow,
            model_class=self.model_class,
            serializer=self.serializer,
        )

    def find_by_email(self, email: str) -> shared_behavior.M | None:
        query = FIND_BY_EMAIL_QUERY.format(table_name=self.table_name)
        return psycopg_commons.execute_query(
            query=query,
            params=(email,),
            uow=self.uow,
            model_class=self.model_class,
            serializer=self.serializer,
        )


class PsycopgAuthFinderRepository(PsycopgAuthBaseFinderRepository[domain_auth.AuthUser, domain_auth_id.AuthId]):
    def __init__(self, uow: shared_uow.UOW) -> None:
        super().__init__(
            table_name=psycopg_user_commons.TABLE_NAME,
            uow=uow,
            model_class=domain_auth.AuthUser,
            serializer=psycopg_commons.BasicTypeSerializer()
        )
