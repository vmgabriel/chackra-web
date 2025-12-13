import pydantic

from chackra_web.user.domain.models import user as domain_user


class CreateUserDTO(pydantic.BaseModel):
    username: str
    name: str
    last_name: str
    email: str


class CreateUserCommand:
    def __init__(self, requirements: ...) -> None:
        ...

    def execute(self, create_user_dto: CreateUserDTO) -> domain_user.User:
        user_created = domain_user.User.create(
            user_data=domain_user.UserCreateDTO(
                username=create_user_dto.username,
                name=create_user_dto.name,
                last_name=create_user_dto.last_name,
                email=create_user_dto.email
            )
        )

        # Persistence
        # Send Events

        return user_created