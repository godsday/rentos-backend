from datetime import date
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.modules.rentals.models import RentalStatus


class CreateRentalRequest(BaseModel):
    # Customer renting the item(s).
    customer_id: UUID

    # Rental start date.
    rental_date: date

    # Expected return date.
    expected_return_date: date

    # Security deposit collected from customer.
    security_deposit: Decimal = Field(
        default=Decimal("0.00"),
        ge=0,
    )

    # Optional rental notes.
    notes: str | None = Field(
        default=None,
        max_length=500,
    )

    @model_validator(mode="after")
    def validate_dates(self):
        if self.expected_return_date < self.rental_date:
            raise ValueError(
                "Expected return date cannot be before rental date."
            )

        return self


class UpdateRentalRequest(BaseModel):
    # Expected return date can be changed while rental is active.
    expected_return_date: date | None = None

    # Actual return date.
    actual_return_date: date | None = None

    # Rental status.
    status: RentalStatus | None = None

    # Security deposit can be updated if required.
    security_deposit: Decimal | None = Field(
        default=None,
        ge=0,
    )

    # Optional notes.
    notes: str | None = Field(
        default=None,
        max_length=500,
    )


class RentalResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    tenant_id: UUID
    customer_id: UUID

    rental_date: date
    expected_return_date: date
    actual_return_date: date | None

    total_amount: Decimal
    security_deposit: Decimal

    status: RentalStatus
    notes: str | None