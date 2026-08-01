from app.core.security import hash_password
from app.modules.auth.models import User
from app.modules.auth.repository import UserRepository
from app.modules.auth.schema import CreateUserRequest
from fastapi import HTTPException, status
from app.modules.tenants.models import Tenant
from app.modules.tenants.repository import TenantRepository
from app.common.utils.slug import generate_slug
from app.modules.roles.repository import RoleRepository
from app.modules.tenant_members.models import TenantMember
from app.modules.tenant_members.repository import TenantMemberRepository

from app.core.security import (
    verify_password,
    create_access_token,
)
from app.modules.auth.schema import TokenResponse

class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def register(self, request: CreateUserRequest) -> User:
       try:
        if self.repository.get_by_email(request.email):
             raise HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Email already exists"
)

        if self.repository.get_by_phone(request.phone):
            raise HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Phone already exists"
)

        tenant_repository = TenantRepository(
            self.repository.db,
        )

        slug = generate_slug(
            request.business_name,
        )

        if tenant_repository.get_by_slug(slug):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Business already exists.",
            )
# Create Tenant
        tenant = tenant_repository.create(
            Tenant(
                name=request.business_name,
                slug=slug,
            )
        )
 # Create User
        user = self.repository.create(
        User(
            full_name=request.full_name,
            email=request.email,
            phone=request.phone,
            password_hash=hash_password(request.password),
        )
    )

# Get TENANT_OWNER role      

        role_repository = RoleRepository(
            self.repository.db,
        )

        owner_role = role_repository.get_by_name(
            "TENANT_OWNER"
        )

        if owner_role is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="TENANT_OWNER role not found.",
            )

# Create Tenant Member
        tenant_member_repository = TenantMemberRepository(
    self.repository.db,
)

        tenant_member_repository.create(
        TenantMember(
            tenant_id=tenant.id,
            user_id=user.id,
            role_id=owner_role.id,
        )
    )
        self.repository.db.commit()
        return user
       except Exception:
        self.repository.db.rollback()
        raise
        
    def login(self, email: str, password: str) -> TokenResponse:
        user = self.repository.get_by_email(email)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password.",
            )

        if not verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password.",
            )

        access_token = create_access_token(
            subject=str(user.id),
        )

        return TokenResponse(
            access_token=access_token,
        )