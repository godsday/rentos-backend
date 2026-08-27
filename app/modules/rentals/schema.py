from datetime import date
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field

from app.modules.rentals.models import RentalStatus


class CreateRentalRequest(BaseModel):
    customer_id: UUID
    rental_date: date
    expected_return_date: date

    notes: str | None = Field(
        default=None,
        max_length=500,
    )
class ActivateRentalRequest(BaseModel):
    initial_payment: Decimal = Field(
        default=Decimal("0.00"),
        ge=0,
    )

class UpdateRentalRequest(BaseModel):
    expected_return_date: date | None = None

    

    notes: str | None = Field(
        default=None,
        max_length=500,
    )


class RentalResponse(BaseModel):
    id: UUID
    tenant_id: UUID
    customer_id: UUID

    rental_date: date
    expected_return_date: date
    actual_return_date: date | None

    status: RentalStatus

    total_amount: Decimal
    initial_payment: Decimal

    notes: str | None

    model_config = {
        "from_attributes": True,
    }