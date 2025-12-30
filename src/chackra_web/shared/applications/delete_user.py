import pydantic

from chackra_web.shared.domain.model import extended_dependencies as domain_dependencies

from chackra_web.shared.domain.model.user import user_id as domain_user_id
from chackra_web.shared.domain.model.auth import auth_id as domain_auth_id

from chackra_web.user.application import delete as application_user_delete
from chackra_web.auth.application import delete as application_auth_delete


class DeleteUserDTO(pydantic.BaseModel):
    user_id: domain_user_id.UserId


class ApplicationDeleteUser:
    dependencies: domain_dependencies.ExtendedControllerDependencies

    def __init__(self, dependencies: domain_dependencies.ExtendedControllerDependencies) -> None:
        self.dependencies = dependencies

    def execute(self, delete_user_dto: DeleteUserDTO) -> None:
        application_user_delete.DeleteUserCommand(
            dependencies=self.dependencies
        ).execute(
            application_user_delete.DeleteUserDTO(user_id=delete_user_dto.user_id)
        )

        application_auth_delete.DeleteAuthCommand(dependencies=self.dependencies).execute(
            application_auth_delete.DeleteUserDTO(user_id=delete_user_dto.user_id)
        )

        return None
