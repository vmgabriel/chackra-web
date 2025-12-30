from typing import Type

from chackra_web.shared.domain.model.uow import uow as shared_uow
from chackra_web.shared.domain.model.behavior import behavior as shared_behavior
from chackra_web.shared.infraestructure.repositories.psycopg import (
    commons as psycopg_commons
)
from chackra_web.user.domain.models import behavior as user_behavior
from chackra_web.user.domain.models import user as domain_user
from chackra_web.shared.domain.model.user import user_id as domain_user_id
from chackra_web.user.infraestructure.repositories.psycopg import commons as psycopg_user_commons


FIND_BY_ID_QUERY = """
SELECT
    tu.*, ta.auth_role
FROM {table_name} as tu
LEFT JOIN tbl_auth as ta ON ta.user_id = tu.id
WHERE tu.id = %s AND tu.active = true;
"""
FIND_BY_EMAIL_QUERY = """
SELECT
    tu.*, ta.auth_role
FROM {table_name} as tu
LEFT JOIN tbl_auth as ta ON ta.user_id = tu.id
WHERE tu.email = %s AND tu.active = true;
"""
FIND_BY_USERNAME_QUERY = """
SELECT
    tu.*, ta.auth_role
FROM tbl_user as tu
LEFT JOIN tbl_auth as ta ON ta.user_id = tu.id
WHERE tu.username = %s AND tu.active = true;
"""
FIND_BY_USERNAME_AND_EMAIL_QUERY = """
SELECT
    tu.*, ta.auth_role
FROM {table_name} as tu
LEFT JOIN tbl_auth as ta ON ta.user_id = tu.id
WHERE tu.username = %s OR tu.email = %s;
"""


class PsycopgUserBaseFinderRepository(
    shared_behavior.FinderBehavior[shared_behavior.M, shared_behavior.ID],
    user_behavior.EmailFinderBehavior[shared_behavior.M],
    user_behavior.UsernameFinderBehavior[shared_behavior.M],
    user_behavior.UniqueUsernameEmailFinderBehavior[shared_behavior.M],
):
    table_name: str
    uow: shared_uow.UOW
    serializer: psycopg_commons.SafeSerializer
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
            params=(id.value,),
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

    def find_by_username(self, username: str) -> shared_behavior.M | None:
        query = FIND_BY_USERNAME_QUERY.format(table_name=self.table_name)
        return psycopg_commons.execute_query(
            query=query,
            params=(username,),
            uow=self.uow,
            model_class=self.model_class,
            serializer=self.serializer,
        )

    def find_unique_by_username_and_email(self, username: str, email: str) -> shared_behavior.M | None:
        query = FIND_BY_USERNAME_AND_EMAIL_QUERY.format(table_name=self.table_name)
        return psycopg_commons.execute_query(
            query=query,
            params=(username, email),
            uow=self.uow,
            model_class=self.model_class,
            serializer=self.serializer,
        )


class PsycopgUserFinderRepository(PsycopgUserBaseFinderRepository[domain_user.User, domain_user_id.UserId]):
    def __init__(self, uow: shared_uow.UOW) -> None:
        super().__init__(
            table_name=psycopg_user_commons.TABLE_NAME,
            uow=uow,
            model_class=domain_user.User,
            serializer=psycopg_commons.BasicTypeSerializer()
        )
