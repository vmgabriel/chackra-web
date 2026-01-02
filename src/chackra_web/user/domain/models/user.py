import pydantic
import uuid
import datetime

from chackra_web.shared.domain.model.user import user_id as domain_user_id
from chackra_web.shared.domain.model.auth import enums as auth_enums


class UserCreateDTO(pydantic.BaseModel):
    username: str
    name: str
    last_name: str
    email: str


class User(pydantic.BaseModel):
    id: domain_user_id.UserId
    name: str
    last_name: str
    email: str
    username: str
    auth_role: auth_enums.AuthRole = auth_enums.AuthRole.USER
    active: bool = True

    created_at: datetime.datetime = datetime.datetime.now()
    updated_at: datetime.datetime = datetime.datetime.now()
    deleted_at: datetime.datetime | None = None

    @staticmethod
    def create(user_data: UserCreateDTO) -> "User":
        return User(
            id=domain_user_id.UserId(value=str(uuid.uuid4())),
            name=user_data.name,
            last_name=user_data.last_name,
            username=user_data.username,
            email=user_data.email,
        )

    @property
    def full_name(self) -> str:
        return f"{self.name} {self.last_name}"

    @property
    def initials(self) -> str:
        return "".join([self.name[0], self.last_name[0]])

    def deactivate(self) -> None:
        self.active = False
        self.updated_at = datetime.datetime.now()
        self.deleted_at = datetime.datetime.now()

    def model_dump(self, *args, **kwargs) -> dict:
        values = super().model_dump(*args, **kwargs)
        values.pop("auth_role")
        return values
