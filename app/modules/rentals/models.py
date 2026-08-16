import enum
import uuid

from sqlalchemy import Boolean, Date, Enum, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_entity import BaseEntity


class RentalStatus(str, enum.Enum):
    PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    RETURNED = "RETURNED"
    CANCELLED = "CANCELLED"


class Rental(BaseEntity):
    __tablename__ = "rentals"

    # Tenant that owns this rental transaction.
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("tenants.id"),
        nullable=False,
        index=True,
    )

    # Customer who rented the item(s).
    customer_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("customers.id"),
        nullable=False,
        index=True,
    )

    # Date on which the rental starts.
    rental_date: Mapped[object] = mapped_column(
        Date,
        nullable=False,
    )

    # Expected date on which the customer should return the rental.
    expected_return_date: Mapped[object] = mapped_column(
        Date,
        nullable=False,
    )

    # Actual return date. NULL while rental is active.
    actual_return_date: Mapped[object | None] = mapped_column(
        Date,
        nullable=True,
    )

    # Total rental amount.
    total_amount: Mapped[float] = mapped_column(
        Numeric(10, 2),
        nullable=False,
        default=0,
    )

    # Security deposit collected for this rental.
    security_deposit: Mapped[float] = mapped_column(
        Numeric(10, 2),
        nullable=False,
        default=0,
    )

    # Current rental lifecycle status.
    status: Mapped[RentalStatus] = mapped_column(
        Enum(RentalStatus, name="rental_status"),
        nullable=False,
        default=RentalStatus.PENDING,
    )

    # Optional notes for the rental.
    notes: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )