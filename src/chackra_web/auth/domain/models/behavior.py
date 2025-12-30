from typing import Protocol

from chackra_web.shared.domain.model.behavior import behavior as shared_behavior
from chackra_web.shared.domain.model.auth import enums as auth_enums
from chackra_web.shared.domain.model.user import user_id as domain_user_id


class EmailFinderBehavior(Protocol[shared_behavior.M]):
    def find_by_email(self, email: str) -> shared_behavior.M | None:
        raise NotImplementedError()


class UserIDFinderBehavior(Protocol[shared_behavior.M]):
    def find_by_user_id(self, user_id: domain_user_id.UserId) -> shared_behavior.M | None:
        raise NotImplementedError()


class ChangeRoleBehavior(Protocol[shared_behavior.ID]):
    def change_role(self, id: shared_behavior.ID, role: auth_enums.AuthRole) -> None:
        raise NotImplementedError()


class AuthFinderBehavior(
    shared_behavior.FinderBehavior[shared_behavior.M, shared_behavior.ID],
    EmailFinderBehavior[shared_behavior.M],
    UserIDFinderBehavior[shared_behavior.M],
):
    ...


class AuthUpdaterBehavior(
    shared_behavior.UpdaterBehavior[shared_behavior.M, shared_behavior.ID],
    ChangeRoleBehavior[shared_behavior.ID],
):
    ...