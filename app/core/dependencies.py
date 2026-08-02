from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.db.session import get_db

from app.modules.auth.repository import UserRepository
from app.modules.tenant_members.repository import TenantMemberRepository
from app.modules.roles.repository import RoleRepository
from app.modules.tenants.repository import TenantRepository


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login",
)


def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    payload = decode_access_token(token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    user_id = payload.get("sub")

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    # Load User
    user_repository = UserRepository(db)

    user = user_repository.get_by_id(
        UUID(user_id),
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    # Load Tenant Membership
    tenant_member_repository = TenantMemberRepository(db)

    membership = tenant_member_repository.get_by_user_id(
        user.id,
    )

    if membership is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tenant membership not found.",
        )

    # Load Role
    role_repository = RoleRepository(db)

    role = role_repository.get_by_id(
        membership.role_id,
    )

    # Load Tenant
    tenant_repository = TenantRepository(db)

    tenant = tenant_repository.get_by_id(
        membership.tenant_id,
    )

    # Attach extra properties
    user.tenant_id = tenant.id
    user.tenant_name = tenant.name
    user.role = role.name

    return user