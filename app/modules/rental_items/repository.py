from decimal import Decimal
import uuid

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.db.base_repository import BaseRepository
from app.modules.rental_items.models import RentalItem


class RentalItemRepository(BaseRepository[RentalItem]):
    def __init__(self, db: Session):
        super().__init__(db, RentalItem)

    def get_by_rental(
        self,
        rental_id: uuid.UUID,
    ) -> list[RentalItem]:
        statement = (
            select(RentalItem)
            .where(
                RentalItem.rental_id == rental_id,
                RentalItem.is_deleted.is_(False),
            )
            .order_by(RentalItem.created_at)
        )

        return list(self.db.scalars(statement).all())

    def get_by_rental_and_item(
        self,
        rental_id: uuid.UUID,
        item_id: uuid.UUID,
    ) -> RentalItem | None:
        statement = select(RentalItem).where(
            RentalItem.rental_id == rental_id,
            RentalItem.item_id == item_id,
            RentalItem.is_deleted.is_(False),
        )

        return self.db.scalar(statement)

    def get_total_by_rental(
        self,
        rental_id: uuid.UUID,
    ) -> Decimal:

        statement = select(
            func.coalesce(
                func.sum(RentalItem.subtotal),
                0,
            )
        ).where(
            RentalItem.rental_id == rental_id,
            RentalItem.is_deleted.is_(False),
        )

        return self.db.scalar(statement) or Decimal("0.00")