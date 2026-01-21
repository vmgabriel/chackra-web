from chackra_web.shared.domain.model.uow import uow as shared_uow
from chackra_web.shared.infraestructure.repositories.psycopg import (
    generics as psycopg_generics,
    commons as psycopg_commons
)
from chackra_web.user.domain.models import user as domain_user, additional_user as domain_additional_user
from chackra_web.user.infraestructure.repositories.psycopg import commons as psycopg_user_commons


class PsycopgUserCreatorRepository(psycopg_generics.PsycopgGenericCreator[domain_user.User]):
    def __init__(self, uow: shared_uow.UOW) -> None:
        super().__init__(
            table_name=psycopg_user_commons.TABLE_NAME,
            uow=uow,
            serializer=psycopg_commons.BasicTypeSerializer()
        )


class PsycopgAdditionalInformationUserCreatorRepository(
    psycopg_generics.PsycopgGenericCreator[domain_additional_user.UserAdditionalInformation]
):
    def __init__(self, uow: shared_uow.UOW) -> None:
        super().__init__(
            table_name=psycopg_user_commons.ADDITIONAL_TABLE_NAME,
            uow=uow,
            serializer=psycopg_user_commons.AdditionalInformationUserSerializer()
        )
