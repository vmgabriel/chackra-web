from chackra_web.shared.domain.model import dependencies as shared_dependencies
from chackra_web.shared.domain.model.behavior import behavior as shared_behavior
from chackra_web.shared.domain.model.repository import repository as shared_repository

from chackra_web.user.domain.models.behavior import UserFinderBehavior


class UserBaseRepository(shared_repository.GenericRepository[shared_behavior.M, shared_behavior.ID]):
    def __init__(
        self,
        dependencies: shared_dependencies.ControllerDependencies,
        creator: shared_behavior.CreatorBehavior[shared_behavior.M],
        finder: UserFinderBehavior[shared_behavior.M, shared_behavior.ID],
    ):
        super().__init__(dependencies, creator, finder)
        self._email_finder = finder
        self._username_finder = finder
        self._unique_username_email_finder = finder


    def find_by_email(self, email: str) -> shared_behavior.M | None:
        return self._email_finder.find_by_email(email)

    def find_by_username(self, username: str) -> shared_behavior.M | None:
        return self._username_finder.find_by_username(username)

    def find_unique_by_username_and_email(self, username: str, email: str) -> shared_behavior.M | None:
        return self._unique_username_email_finder.find_unique_by_username_and_email(username, email)
