from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_entity import BaseEntity


class Tenant(BaseEntity):
    __tablename__ = "tenants"

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    slug: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        index=True,
        nullable=False,
    )

    logo: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        default=True,
        nullable=False,
    )