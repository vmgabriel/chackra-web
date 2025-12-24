from typing import Protocol

from chackra_web.shared.domain.model.behavior import behavior as shared_behavior


class EmailFinderBehavior(Protocol[shared_behavior.M]):
    def find_by_email(self, email: str) -> shared_behavior.M | None:
        raise NotImplementedError()


class AuthFinderBehavior(
    shared_behavior.FinderBehavior[shared_behavior.M, shared_behavior.ID],
    EmailFinderBehavior[shared_behavior.M],
):
    ...