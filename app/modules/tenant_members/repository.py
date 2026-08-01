from app.db.base_repository import BaseRepository
from app.modules.tenant_members.models import TenantMember


class TenantMemberRepository(BaseRepository[TenantMember]):
    model = TenantMember

    def __init__(self, db):
        super().__init__(db, TenantMember)