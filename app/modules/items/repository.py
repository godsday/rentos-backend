from uuid import UUID

from app.db.base_repository import BaseRepository
from app.modules.items.models import Item


class ItemRepository(BaseRepository[Item]):
    """
    Repository responsible for all Item database operations.
    """

    def __init__(self, db):
        super().__init__(db, Item)

    def get_by_name(
        self,
        tenant_id: UUID,
        name: str,
    ):
        return (
            self.db.query(Item)
            .filter(
                Item.tenant_id == tenant_id,
                Item.name == name,
                Item.is_deleted.is_(False),
            )
            .first()
        )

    def get_by_sku(
        self,
        tenant_id: UUID,
        sku: str,
    ):
        return (
            self.db.query(Item)
            .filter(
                Item.tenant_id == tenant_id,
                Item.sku == sku,
                Item.is_deleted.is_(False),
            )
            .first()
        )

    def get_by_category(
        self,
        tenant_id: UUID,
        category_id: UUID,
    ):
        return (
            self.db.query(Item)
            .filter(
                Item.tenant_id == tenant_id,
                Item.category_id == category_id,
                Item.is_deleted.is_(False),
            )
            .order_by(Item.name)
            .all()
        )

    def get_all_by_tenant(
        self,
        tenant_id,
        page: int,
        limit: int,
        search: str | None = None,
        sort: str = "name"

        
    ):
        query = (
            self.db.query(Item)
            .filter(
                Item.tenant_id == tenant_id,
                Item.is_deleted.is_(False),
            )
        )

        if search:
            query = query.filter(
                Item.name.ilike(f"%{search}%")
            )
        sort_columns = {
            "name": Item.name,
            "sku": Item.sku,
            "rental_price": Item.rental_price,
            "quantity": Item.quantity,
            "created_at": Item.created_at,
        }

        

        offset = (page - 1) * limit

        return (
            query.order_by(
              sort_columns.get(sort,  Item.name))
            .offset(offset)
            .limit(limit)
            .all()
        )

    def get_by_sku(
        self,
        tenant_id,
        sku,
    ):
        return (
            self.db.query(Item)
            .filter(
                Item.tenant_id == tenant_id,
                Item.sku == sku,
                Item.is_deleted.is_(False),
            )
            .first()
        )