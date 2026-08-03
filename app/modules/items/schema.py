from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class CreateItemRequest(BaseModel):
    """
    Request model for creating a new rental item.
    """

    category_id: UUID
    name: str
    sku: str
    description: str | None = None
    rental_price: Decimal
    security_deposit: Decimal = Decimal("0")
    quantity: int
    barcode: str | None = None
    image: str | None = None


class UpdateItemRequest(BaseModel):
    """
    Request model for updating an existing rental item.
    """

    category_id: UUID
    name: str
    sku: str
    description: str | None = None
    rental_price: Decimal
    security_deposit: Decimal
    quantity: int
    barcode: str | None = None
    image: str | None = None
    is_active: bool


class ItemResponse(BaseModel):
    """
    API response returned after creating/updating/fetching an item.
    """

    id: UUID
    category_id: UUID
    name: str
    sku: str
    description: str | None
    rental_price: Decimal
    security_deposit: Decimal
    quantity: int
    available_quantity: int
    barcode: str | None
    image: str | None
    is_active: bool

    model_config = ConfigDict(
        from_attributes=True,
    )