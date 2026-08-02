from app.db.base_repository import BaseRepository
from app.modules.tenants.models import Tenant
from uuid import UUID


class TenantRepository(BaseRepository[Tenant]):
    model = Tenant

    def __init__(self, db):
        super().__init__(db, Tenant)
    
    def get_by_id(
        self,
        tenant_id: UUID,
    ):
        return (
            self.db.query(Tenant)
            .filter(
                Tenant.id == tenant_id,
                Tenant.is_deleted.is_(False),
            )
            .first()
        )

    def get_by_slug(self, slug: str):
        return (
            self.db.query(Tenant)
            .filter(
                Tenant.slug == slug,
                Tenant.is_deleted.is_(False),
            )
            .first()
        )