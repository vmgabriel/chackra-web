from chackra_web.shared.domain.model.exceptions import exception as shared_exception

import enum


class ExceptionCodeError(enum.StrEnum):
    INVENTORY_ITEM_HAS_ALREADY_REGISTERED = "inventory_item_has_already_registered"
    INVENTORY_ITEM_NOT_FOUND = "inventory_item_not_found"
    INVENTORY_ITEM_HAS_ALREADY_DELETED = "inventory_item_has_already_deleted"
    TO_BUY_ITEM_HAS_ALREADY_REGISTERED = "to_boy_item_has_already_registered"


class InventoryItemExistsException(shared_exception.SystemException):
    def __init__(self) -> None:
        message = shared_exception.ExceptionMessage(
            title="El Item ya existe en el inventario",
            description="El item ya existe en el inventario, no se va a registrar",
            code=str(ExceptionCodeError.INVENTORY_ITEM_HAS_ALREADY_REGISTERED.value),
        )
        super().__init__(message=message, status_code=400)


class InventoryItemNotExistsException(shared_exception.SystemException):
    def __init__(self) -> None:
        message = shared_exception.ExceptionMessage(
            title="El item no existe en el inventario",
            description="Se requiere la existencia del inventory item",
            code=str(ExceptionCodeError.INVENTORY_ITEM_NOT_FOUND.value),
        )
        super().__init__(message=message, status_code=404)


class InventoryItemHasAlreadyDeletedException(shared_exception.SystemException):
    def __init__(self) -> None:
        message = shared_exception.ExceptionMessage(
            title="El Item del inventario ya ha sido borrado",
            description="No se requiere eliminar, ya esta eliminado",
            code=str(ExceptionCodeError.INVENTORY_ITEM_HAS_ALREADY_DELETED.value),
        )
        super().__init__(message=message, status_code=404)


class ToBuyItemHasAlreadyRegisteredException(shared_exception.SystemException):
    def __init__(self) -> None:
        message = shared_exception.ExceptionMessage(
            title="El Item ya esta en la lista de compras",
            description="El item ya existe en la lista de compras",
            code=str(ExceptionCodeError.TO_BUY_ITEM_HAS_ALREADY_REGISTERED.value),
        )
        super().__init__(message=message, status_code=400)
