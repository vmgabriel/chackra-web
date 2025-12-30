from chackra_web.shared.domain.model.exceptions import exception as shared_exception

import enum


class ExceptionCodeError(enum.StrEnum):
    INVENTORY_ITEM_HAS_ALREADY_REGISTERED = "inventory_item_has_already_registered"


class InventoryItemExistsException(shared_exception.SystemException):
    def __init__(self) -> None:
        message = shared_exception.ExceptionMessage(
            title="El Item ya existe en el inventario",
            description="El item ya existe en el inventario, no se va a registrar",
            code=str(ExceptionCodeError.INVENTORY_ITEM_HAS_ALREADY_REGISTERED.value),
        )
        super().__init__(message=message, status_code=400)
