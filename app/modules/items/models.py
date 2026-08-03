from uuid import UUID

from sqlalchemy import (
    Boolean,
    ForeignKey,
    Numeric,
    String,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_entity import BaseEntity
from sqlalchemy import (
    ForeignKey,
    UniqueConstraint,
)


class Item(BaseEntity):
    """
    Represents a rentable item belonging to a tenant.

    Used By:
    - Rental Orders
    - Inventory
    - Dashboard
    """

    __tablename__ = "items"

    tenant_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("tenants.id"),
        nullable=False,
    )

    category_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("categories.id"),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    sku: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
      
    )

    description: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    rental_price: Mapped[float] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    security_deposit: Mapped[float] = mapped_column(
        Numeric(10, 2),
        nullable=False,
        default=0,
    )

    quantity: Mapped[int] = mapped_column(
        nullable=False,
    )

    available_quantity: Mapped[int] = mapped_column(
        nullable=False,
    )

    barcode: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    image: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )
    __table_args__ = (
    UniqueConstraint(
        "tenant_id",
        "sku",
        name="uq_item_tenant_sku",
    ),
)