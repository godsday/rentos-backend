import uuid
from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_entity import BaseEntity


class RentalItem(BaseEntity):
    __tablename__ = "rental_items"

    rental_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("rentals.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    item_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("items.id"),
        nullable=False,
        index=True,
    )

    quantity: Mapped[int] = mapped_column(
        nullable=False,
         default=1,
    )

    rental_price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
        default=Decimal("0.00"),
    )


    subtotal: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
        default=Decimal("0.00"),
    )

    rental = relationship(
        "Rental",
        back_populates="items",
    )