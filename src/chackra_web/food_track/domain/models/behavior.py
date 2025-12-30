from typing import Protocol

from chackra_web.shared.domain.model.behavior import behavior as shared_behavior


class NameFinderBehavior(Protocol[shared_behavior.M]):
    def find_by_name(self, name: str) -> shared_behavior.M | None:
        raise NotImplementedError()


class InventoryFinderBehavior(
    shared_behavior.FinderBehavior[shared_behavior.M, shared_behavior.ID],
    NameFinderBehavior[shared_behavior.M],
):
    ...