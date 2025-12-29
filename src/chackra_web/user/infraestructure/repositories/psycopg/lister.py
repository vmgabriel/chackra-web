from chackra_web.shared.domain.model.uow import uow as shared_uow
from chackra_web.shared.infraestructure.repositories.psycopg import (
    generics as psycopg_generics,
    commons as psycopg_commons
)
from chackra_web.user.domain.models import user as domain_user
from chackra_web.user.infraestructure.repositories.psycopg import commons as psycopg_user_commons


class PsycopgUserListerRepository(psycopg_generics.PsycopgGenericLister[domain_user.User]):
    def __init__(self, uow: shared_uow.UOW) -> None:
        super().__init__(
            table_name=psycopg_user_commons.TABLE_NAME,
            uow=uow,
            serializer=psycopg_commons.BasicTypeSerializer(),
            model_class=domain_user.User,
        )
