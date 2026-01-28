import pydantic
import datetime
import uuid
import enum

from chackra_web.shared.domain.model.user import user_id, additional_user_id


class GenderType(enum.StrEnum):
    MALE = "Male"
    FEMALE = "Female"


class LifestyleType(enum.StrEnum):
    VERY_ATLETIC = "Very Atletic"
    ATLETIC = "Atletic"
    BALANCED = "Balance"
    SEDENTARY = "Sedentary"
    VERY_SEDENTARY = "Very Sedentary"

    @staticmethod
    def get_lifestyle_type(ref: int) -> "LifestyleType":
        values = {
            0: LifestyleType.VERY_SEDENTARY,
            1: LifestyleType.SEDENTARY,
            2: LifestyleType.BALANCED,
            3: LifestyleType.ATLETIC,
            4: LifestyleType.VERY_ATLETIC,
        }
        return values[ref]

    @staticmethod
    def get_by_name(name: str) -> "LifestyleType":
        return LifestyleType(name.title())


class DaySchedule(pydantic.BaseModel):
    start: datetime.time
    end: datetime.time


class WorkSchedule(pydantic.BaseModel):
    monday: DaySchedule
    tuesday: DaySchedule
    wednesday: DaySchedule
    thursday: DaySchedule
    friday: DaySchedule
    saturday: DaySchedule
    sunday: DaySchedule


class CreateUserAdditionalInformation(pydantic.BaseModel):
    user_id: user_id.UserId
    birth_date: datetime.date
    genre: GenderType
    country: str
    height: float
    weight: float

    profession: str
    work_schedule: WorkSchedule

    health_difficulties: str
    allergenic_products: str
    lifestyle: LifestyleType
    with_oven: bool
    foods: list[str]

    sleep_phase: DaySchedule


class UpdateUserAdditionalInformation(CreateUserAdditionalInformation):
    ...


class UserAdditionalInformation(pydantic.BaseModel):
    id: additional_user_id.AdditionalUserId
    user_id: user_id.UserId
    birth_date: datetime.date
    genre: GenderType
    country: str
    height: float
    weight: float

    profession: str
    work_schedule: WorkSchedule

    health_difficulties: str
    allergenic_products: str
    lifestyle: LifestyleType
    with_oven: bool
    foods: list[str]

    sleep_phase: DaySchedule

    active: bool = True
    created_at: datetime.datetime = datetime.datetime.now()
    updated_at: datetime.datetime = datetime.datetime.now()
    deleted_at: datetime.datetime | None = None

    @staticmethod
    def create(create_dto: CreateUserAdditionalInformation) -> "UserAdditionalInformation":
        return UserAdditionalInformation(
            id=additional_user_id.AdditionalUserId(value=str(uuid.uuid4())),
            user_id=create_dto.user_id,
            birth_date=create_dto.birth_date,
            genre=create_dto.genre,
            country=create_dto.country,
            height=create_dto.height,
            weight=create_dto.weight,
            profession=create_dto.profession,
            work_schedule=create_dto.work_schedule,
            health_difficulties=create_dto.health_difficulties,
            allergenic_products=create_dto.allergenic_products,
            lifestyle=create_dto.lifestyle,
            with_oven=create_dto.with_oven,
            sleep_phase=create_dto.sleep_phase,
            foods=create_dto.foods,
        )

    def update(self, update_dto: UpdateUserAdditionalInformation) -> "UserAdditionalInformation":
        self.user_id = update_dto.user_id
        self.birth_date = update_dto.birth_date
        self.genre = update_dto.genre
        self.country = update_dto.country
        self.height = update_dto.height
        self.weight = update_dto.weight
        self.profession = update_dto.profession
        self.work_schedule = update_dto.work_schedule
        self.health_difficulties = update_dto.health_difficulties
        self.allergenic_products = update_dto.allergenic_products
        self.lifestyle = update_dto.lifestyle
        self.with_oven = update_dto.with_oven
        self.sleep_phase = update_dto.sleep_phase

        self.updated_at = datetime.datetime.now()
        return self

    def birth_year(self) -> int:
        current_datetime = datetime.datetime.now().date()
        return (current_datetime - self.birth_date).days // 365

    def model_dump(self, *args, **kwargs) -> dict:
        values = super().model_dump(*args, **kwargs)
        values["foods"] = ",".join(self.foods)
        return values
