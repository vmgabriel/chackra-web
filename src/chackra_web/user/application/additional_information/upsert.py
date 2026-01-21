import pydantic
import datetime

from chackra_web.shared.domain.model.uow import uow as shared_uow
from chackra_web.shared.domain.model.logger import logger as shared_logger

from chackra_web.shared.domain.model import extended_dependencies as domain_dependencies
from chackra_web.shared.domain.model.user import additional_user_id, user_id
from chackra_web.shared.domain.model.configuration import configuration as shared_configuration

from chackra_web.user.domain.models import (
    additional_user as additional_user_domain,
    repositories as user_repositories
)
from chackra_web.user.domain.services.additional_information import upsert as services_upsert


class UpsertAdditionalInformationUser(pydantic.BaseModel):
    user_id: user_id.UserId
    birth_date: datetime.date
    gender: str
    country: str
    height: float
    weight: float
    profession: str
    work_schedule: dict[str, dict[str, str]]
    difficulties: str
    allergic_product: str
    lifestyle_product: str
    foods: list[str]
    sleep_time: dict[str, str]
    with_oven: bool


class UpsertAdditionalInformationUserCommand:
    uow: shared_uow.UOW
    logger: shared_logger.LogAdapter
    additional_user_repository:  user_repositories.AdditionalUserRepository[
        additional_user_domain.UserAdditionalInformation,
        additional_user_id.AdditionalUserId
    ]
    configuration: shared_configuration.Configuration

    def __init__(self, dependencies: domain_dependencies.ExtendedControllerDependencies):
        self.uow = dependencies.uow
        self.logger = dependencies.logger
        self.additional_user_repository = dependencies.repository_store.build(
            user_repositories.AdditionalUserRepository[
                additional_user_domain.UserAdditionalInformation,
                additional_user_id.AdditionalUserId
            ]
        )
        self.configuration = dependencies.configuration

    def execute(self, upsert_dto: UpsertAdditionalInformationUser) -> additional_user_domain.UserAdditionalInformation:
        work_schedule = additional_user_domain.WorkSchedule(
            monday=additional_user_domain.DaySchedule(
                start=datetime.datetime.strptime(
                    upsert_dto.work_schedule.get("monday", {}).get("start"),
                    self.configuration.time_format
                ).time(),
                end=datetime.datetime.strptime(
                    upsert_dto.work_schedule.get("monday", {}).get("end"),
                    self.configuration.time_format
                ).time(),
            ),
            tuesday=additional_user_domain.DaySchedule(
                start=datetime.datetime.strptime(
                    upsert_dto.work_schedule.get("tuesday", {}).get("start"),
                    self.configuration.time_format
                ).time(),
                end=datetime.datetime.strptime(
                    upsert_dto.work_schedule.get("tuesday", {}).get("end"),
                    self.configuration.time_format
                ).time(),
            ),
            wednesday=additional_user_domain.DaySchedule(
                start=datetime.datetime.strptime(
                    upsert_dto.work_schedule.get("wednesday", {}).get("start"),
                    self.configuration.time_format
                ).time(),
                end=datetime.datetime.strptime(
                    upsert_dto.work_schedule.get("wednesday", {}).get("end"),
                    self.configuration.time_format
                ).time(),
            ),
            thursday=additional_user_domain.DaySchedule(
                start=datetime.datetime.strptime(
                    upsert_dto.work_schedule.get("thursday", {}).get("start"),
                    self.configuration.time_format
                ).time(),
                end=datetime.datetime.strptime(
                    upsert_dto.work_schedule.get("thursday", {}).get("end"),
                    self.configuration.time_format
                ).time()
            ),
            friday=additional_user_domain.DaySchedule(
                start=datetime.datetime.strptime(
                    upsert_dto.work_schedule.get("friday", {}).get("start"),
                    self.configuration.time_format
                ).time(),
                end=datetime.datetime.strptime(
                    upsert_dto.work_schedule.get("friday", {}).get("end"),
                    self.configuration.time_format
                ).time()
            ),
            saturday=additional_user_domain.DaySchedule(
                start=datetime.datetime.strptime(
                    upsert_dto.work_schedule.get("saturday", {}).get("start"),
                    self.configuration.time_format
                ).time(),
                end=datetime.datetime.strptime(
                    upsert_dto.work_schedule.get("saturday", {}).get("end"),
                    self.configuration.time_format
                ).time()
            ),
            sunday=additional_user_domain.DaySchedule(
                start=datetime.datetime.strptime(
                    upsert_dto.work_schedule.get("sunday", {}).get("start"),
                    self.configuration.time_format
                ).time(),
                end=datetime.datetime.strptime(
                    upsert_dto.work_schedule.get("sunday", {}).get("end"),
                    self.configuration.time_format
                ).time()
            )
        )
        lifestyle = additional_user_domain.LifestyleType.get_by_name(upsert_dto.lifestyle_product)

        update_additional_information = additional_user_domain.UpdateUserAdditionalInformation(
            user_id=upsert_dto.user_id,
            birth_date=upsert_dto.birth_date,
            genre=additional_user_domain.GenderType(upsert_dto.gender.capitalize()),
            country=upsert_dto.country,
            height=upsert_dto.height,
            weight=upsert_dto.weight,
            profession=upsert_dto.profession,
            work_schedule=work_schedule,
            health_difficulties=upsert_dto.difficulties,
            allergenic_products=upsert_dto.allergic_product,
            lifestyle=lifestyle,
            with_oven=upsert_dto.with_oven,
            sleep_phase=additional_user_domain.DaySchedule(
                start=datetime.datetime.strptime(
                    upsert_dto.sleep_time.get("start", "00:00"),
                    self.configuration.time_format
                ).time(),
                end=datetime.datetime.strptime(
                    upsert_dto.sleep_time.get("end", "00:00"),
                    self.configuration.time_format
                ).time(),
            ),
            foods=upsert_dto.foods
        )

        updated_additional_information = services_upsert.upsert(
            update_additional_information=update_additional_information,
            additional_user_repository=self.additional_user_repository,
        )
        return updated_additional_information
