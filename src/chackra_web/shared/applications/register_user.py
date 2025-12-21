import pydantic
import datetime

from chackra_web.shared.domain.model.user import user_id as domain_user_id
from chackra_web.user.application import create as application_user_create
from chackra_web.auth.application import create as application_auth_create

from chackra_web.shared.domain.model import extended_dependencies as domain_dependencies


class RegisterUserDTO(pydantic.BaseModel):
    email: str
    password: str
    name: str
    last_name: str
    username: str


class RegisterUserResponse(pydantic.BaseModel):
    auth_id: str
    user_id: domain_user_id.UserId
    email: str
    created_at: datetime.datetime


class ApplicationRegisterUser:
    dependencies: domain_dependencies.ExtendedControllerDependencies
    def __init__(self, dependencies: domain_dependencies.ExtendedControllerDependencies) -> None:
        self.dependencies = dependencies

    def execute(self, register_user_dto: RegisterUserDTO) -> RegisterUserResponse:
        # create user
        create_user_command = application_user_create.CreateUserCommand(dependencies=self.dependencies)
        new_user = create_user_command.execute(application_user_create.CreateUserDTO(
            name=register_user_dto.name,
            last_name=register_user_dto.last_name,
            email=register_user_dto.email,
            username=register_user_dto.username,
        ))

        # create auth
        create_auth_user_command = application_auth_create.AuthRegisterService(dependencies=self.dependencies)

        new_auth = create_auth_user_command.save(application_auth_create.AuthRegisterDTO(
            email=register_user_dto.email,
            password=register_user_dto.password,
            user_id=new_user.id
        ))

        return RegisterUserResponse(
            auth_id=new_auth.id,
            user_id=new_user.id,
            email=new_user.email,
            created_at=new_user.created_at
        )