from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_entity import BaseEntity


class Vendor(BaseEntity):
    __tablename__ = "vendors"

    name: Mapped[str] = mapped_column(String(150), nullable=False)