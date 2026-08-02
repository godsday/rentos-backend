from uuid import UUID
from sqlalchemy.orm import joinedload
from app.db.base_repository import BaseRepository
from app.modules.tenant_members.models import TenantMember


class TenantMemberRepository(BaseRepository[TenantMember]):
    model = TenantMember

    def __init__(self, db):
        super().__init__(db, TenantMember)

    def get_by_user_id(
        self,
        user_id: UUID,
    ) -> TenantMember | None:
        return (
            self.db.query(TenantMember)
            .filter(
                TenantMember.user_id == user_id,
                TenantMember.is_deleted.is_(False),
            )
            .first()
        )

    def get_by_user_and_tenant(
        self,
        user_id: UUID,
        tenant_id: UUID,
    ) -> TenantMember | None:
        return (
            self.db.query(TenantMember)
            .filter(
                TenantMember.user_id == user_id,
                TenantMember.tenant_id == tenant_id,
                TenantMember.is_deleted.is_(False),
            )
            .first()
        )

    def get_user_tenants(
        self,
        user_id: UUID,
    ) -> list[TenantMember]:
        return (
            self.db.query(TenantMember)
            .options(
                joinedload(TenantMember.tenant),
                joinedload(TenantMember.role),
            )
            .filter(
                TenantMember.user_id == user_id,
                TenantMember.is_deleted.is_(False),
            )
            .all()
        )

    def is_member(
        self,
        user_id: UUID,
        tenant_id: UUID,
    ) -> bool:
        return (
            self.get_by_user_and_tenant(
                user_id,
                tenant_id,
            )
            is not None
        )