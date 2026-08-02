from app.db.base_repository import BaseRepository
from app.modules.categories.models import Category


class CategoryRepository(BaseRepository[Category]):
    def __init__(self, db):
        super().__init__(db, Category)

    def get_by_name(self, tenant_id, name):
        return (
            self.db.query(Category)
            .filter(
                Category.tenant_id == tenant_id,
                Category.name == name,
                Category.is_deleted.is_(False),
            )
            .first()
        )

    def get_all_by_tenant(self, tenant_id):
        return (
            self.db.query(Category)
            .filter(
                Category.tenant_id == tenant_id,
                Category.is_deleted.is_(False),
            )
            .order_by(Category.name)
            .all()
        )