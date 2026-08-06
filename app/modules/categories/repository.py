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

    def get_all_by_tenant(
        self, 
        tenant_id,
        page:int, 
        limit: int,
        search: str | None = None,
        sort: str = "name"


     ):
        query = (
            self.db.query(Category)
            .filter(
                Category.tenant_id == tenant_id,
                Category.is_deleted.is_(False),
            )
        )

        if search:
            query = query.filter(
                Category.name.ilike(f"%{search}%")
            )

        sort_columns = {
            "name": Category.name,
            "created_at": Category.created_at,
        }

        query = query.order_by(
            sort_columns.get(sort, Category.name)
        )

        offset = (page - 1) * limit

        return (
            query.order_by(
                sort_columns.get(sort,Category.name))
            .offset(offset)
            .limit(limit)
            .all()
        )