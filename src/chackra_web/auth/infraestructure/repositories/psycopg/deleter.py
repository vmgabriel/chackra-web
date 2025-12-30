from chackra_web.shared.domain.model.uow import uow as shared_uow
from chackra_web.shared.infraestructure.repositories.psycopg import (
    generics as psycopg_generics,
    commons as psycopg_commons
)
from chackra_web.shared.domain.model.auth import auth_id as domain_auth_id
from chackra_web.auth.infraestructure.repositories.psycopg import commons as psycopg_auth_commons


class PsycopgAuthDeleterRepository(psycopg_generics.PsycopgGenericDeleter[domain_auth_id.AuthId]):
    def __init__(self, uow: shared_uow.UOW) -> None:
        super().__init__(
            table_name=psycopg_auth_commons.TABLE_NAME,
            uow=uow,
            serializer=psycopg_commons.BasicTypeSerializer()
        )
