from uuid import UUID

from app.db.base_repository import BaseRepository
from app.modules.rentals.models import Rental


class RentalRepository(BaseRepository[Rental]):
    def __init__(self, db):
        super().__init__(db, Rental)

    def get_all_by_tenant(
        self,
        tenant_id: UUID,
        page: int,
        limit: int,
    ):
        """
        Return paginated rentals belonging to the tenant.
        """

        offset = (page - 1) * limit

        return (
            self.db.query(Rental)
            .filter(
                Rental.tenant_id == tenant_id,
                Rental.is_deleted.is_(False),
            )
            .order_by(Rental.created_at.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )

    def get_by_id_and_tenant(
        self,
        rental_id: UUID,
        tenant_id: UUID,
    ):
        """
        Get a rental only if it belongs to the tenant.
        """

        return (
            self.db.query(Rental)
            .filter(
                Rental.id == rental_id,
                Rental.tenant_id == tenant_id,
                Rental.is_deleted.is_(False),
            )
            .first()
        )