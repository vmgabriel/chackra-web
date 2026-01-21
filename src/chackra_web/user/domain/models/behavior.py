from typing import Protocol

from chackra_web.shared.domain.model.user import user_id
from chackra_web.shared.domain.model.behavior import behavior as shared_behavior


class EmailFinderBehavior(Protocol[shared_behavior.M]):
    def find_by_email(self, email: str) -> shared_behavior.M | None:
        raise NotImplementedError()


class UsernameFinderBehavior(Protocol[shared_behavior.M]):
    def find_by_username(self, username: str) -> shared_behavior.M | None:
        raise NotImplementedError()


class UniqueUsernameEmailFinderBehavior(Protocol[shared_behavior.M]):
    def find_unique_by_username_and_email(self, username: str, email: str) -> shared_behavior.M | None:
        raise NotImplementedError()


class UserIdFinderBehavior(Protocol[shared_behavior.M]):
    def find_by_user_id(self, user_id: user_id.UserId) -> shared_behavior.M | None:
        raise NotImplementedError()


class UserFinderBehavior(
    shared_behavior.FinderBehavior[shared_behavior.M, shared_behavior.ID],
    EmailFinderBehavior[shared_behavior.M],
    UsernameFinderBehavior[shared_behavior.M],
    UniqueUsernameEmailFinderBehavior[shared_behavior.M],
):
    ...


class AdditionalInformationUserFinderBehavior(
    shared_behavior.FinderBehavior[shared_behavior.M, shared_behavior.ID],
    UserIdFinderBehavior[shared_behavior.M],
):
    ...
