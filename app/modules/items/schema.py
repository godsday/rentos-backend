from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict
from pydantic import BaseModel, ConfigDict, Field


class CreateItemRequest(BaseModel):
    """
    Request model for creating a new rental item.
    """

    category_id: UUID
    name: str = Field(min_length=1, max_length=150)
    sku: str = Field(min_length=1, max_length=100)
    description: str | None = None

    rental_price: Decimal = Field(gt=0)
    purchase_price: Decimal = Field(ge=0)

    quantity: int = Field(gt=0)
    barcode: str | None = None
    image: str | None = None


class UpdateItemRequest(BaseModel):
    """
    Request model for updating an existing rental item.
    """

    category_id: UUID
    sku: str
    name : str
    description: str | None = None
    quantity: int = Field(gt=0)
    barcode: str | None = None
    image: str | None = None
    purchase_price : Decimal = Field(ge=0)
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
    purchase_price : Decimal
    quantity: int
    available_quantity: int
    barcode: str | None
    image: str | None
    is_active: bool

    model_config = ConfigDict(
        from_attributes=True,
    )