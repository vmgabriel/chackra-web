from typing import Protocol

from chackra_web.shared.domain.model.behavior import behavior as shared_behavior


class EmailFinderBehavior(Protocol[shared_behavior.M]):
    def find_by_email(self, email: str) -> shared_behavior.M | None: ...


class UsernameFinderBehavior(Protocol[shared_behavior.M]):
    def find_by_username(self, username: str) -> shared_behavior.M | None: ...


class UniqueUsernameEmailFinderBehavior(Protocol[shared_behavior.M]):
    def find_unique_by_username_and_email(self, username: str, email: str) -> shared_behavior.M | None: ...


class UserFinderBehavior(
    shared_behavior.FinderBehavior[shared_behavior.M, shared_behavior.ID],
    EmailFinderBehavior[shared_behavior.M],
    UsernameFinderBehavior[shared_behavior.M],
    UniqueUsernameEmailFinderBehavior[shared_behavior.M],
):
    ...