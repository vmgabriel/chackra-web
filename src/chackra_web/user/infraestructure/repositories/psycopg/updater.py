from chackra_web.user.domain.models import additional_user as domain_additional_user

from chackra_web.shared.domain.model.uow import uow as shared_uow
from chackra_web.shared.domain.model.user import additional_user_id as domain_additional_user_id

from chackra_web.shared.infraestructure.repositories.psycopg import (
    generics as psycopg_generics,
    commons as psycopg_commons
)
from chackra_web.user.infraestructure.repositories.psycopg import commons as psycopg_user_commons


class PsycopgAdditionalInformationUserUpdaterRepository(
    psycopg_generics.PsycopgGenericUpdaterRepository[
        domain_additional_user.UserAdditionalInformation,
        domain_additional_user_id.AdditionalUserId,
    ]
):
    def __init__(self, uow: shared_uow.UOW) -> None:
        super().__init__(
            table_name=psycopg_user_commons.ADDITIONAL_TABLE_NAME,
            uow=uow,
            model_class=domain_additional_user.UserAdditionalInformation,
            serializer=psycopg_user_commons.AdditionalInformationUserSerializer(),
        )
