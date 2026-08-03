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
        tenant_id: UUID,
    ):
        return (
            self.db.query(Item)
            .filter(
                Item.tenant_id == tenant_id,
                Item.is_deleted.is_(False),
            )
            .order_by(Item.name)
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