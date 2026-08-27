from decimal import Decimal
import enum
import uuid

from sqlalchemy import Date, Enum, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_entity import BaseEntity


class RentalStatus(str, enum.Enum):
    DRAFT = "DRAFT"
    ACTIVE = "ACTIVE"
    PARTIALLY_RETURNED = "PARTIALLY_RETURNED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    OVERDUE = "OVERDUE"


class Rental(BaseEntity):
    __tablename__ = "rentals"

    tenant_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("tenants.id"),
        nullable=False,
        index=True,
    )

    customer_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("customers.id"),
        nullable=False,
        index=True,
    )


    rental_date: Mapped[Date] = mapped_column(
        Date,
        nullable=False,
    )

    expected_return_date: Mapped[Date] = mapped_column(
        Date,
        nullable=False,
    )

    actual_return_date: Mapped[Date | None] = mapped_column(
        Date,
        nullable=True,
    )

    status: Mapped[RentalStatus] = mapped_column(
        Enum(RentalStatus, name="rental_status"),
        nullable=False,
        default=RentalStatus.DRAFT,
    )

    total_amount: Mapped[Decimal] = mapped_column(
    Numeric(10, 2),
    nullable=False,
    default=Decimal("0.00"),
    )

    initial_payment: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
        default=Decimal("0.00"),
    )

    remaining_amount: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
        default=Decimal("0.00"),
    )

    notes: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )