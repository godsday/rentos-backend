from uuid import UUID

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_entity import BaseEntity


class Customer(BaseEntity):
    __tablename__ = "customers"

    __table_args__ = (
        UniqueConstraint(
            "tenant_id",
            "phone",
            name="uq_customer_tenant_phone",
        ),
    )

    tenant_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("tenants.id"),
        nullable=False,
    )

    full_name: Mapped[str] = mapped_column(
        nullable=False,
    )

    phone: Mapped[str] = mapped_column(
        nullable=False,
    )

    email: Mapped[str | None] = mapped_column(
        nullable=True,
    )

    address: Mapped[str | None] = mapped_column(
        nullable=True,
    )

    city: Mapped[str | None] = mapped_column(
        nullable=True,
    )

    state: Mapped[str | None] = mapped_column(
        nullable=True,
    )

    country: Mapped[str | None] = mapped_column(
        nullable=True,
    )

    pincode: Mapped[str | None] = mapped_column(
        nullable=True,
    )

    notes: Mapped[str | None] = mapped_column(
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        nullable=False,
        default=True,
    )