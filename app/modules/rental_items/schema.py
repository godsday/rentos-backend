import uuid
from decimal import Decimal

from pydantic import BaseModel, Field


class CreateRentalItemRequest(BaseModel):
    item_id: uuid.UUID
    quantity: int = Field(
        default=1,
        gt=0,
    )


class UpdateRentalItemRequest(BaseModel):
    quantity: int = Field(gt=0)


class RentalItemResponse(BaseModel):
    id: uuid.UUID
    rental_id: uuid.UUID
    item_id: uuid.UUID
    quantity: int
    rental_price: Decimal
    subtotal: Decimal

    model_config = {
        "from_attributes": True,
    }