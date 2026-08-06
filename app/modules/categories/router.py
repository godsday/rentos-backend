from uuid import UUID

from fastapi import APIRouter, Depends ,Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.dependencies import get_current_user

from app.modules.auth.models import User

from app.modules.categories.repository import CategoryRepository
from app.modules.categories.service import CategoryService
from app.modules.categories.schema import (
    CreateCategoryRequest,
    UpdateCategoryRequest,
    CategoryResponse,
)

router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
)


@router.post(
    "",
    response_model=list[CategoryResponse],
)
def create_category(
    request: CreateCategoryRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    service = CategoryService(
        CategoryRepository(db),
    )

    category = service.create(
        current_user.tenant_id,
        request,
    )
    db.commit()  
    
    return category


@router.get(
    "",
    response_model=list[CategoryResponse],
)
def get_categories(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
    search: str | None = Query(None)
):

    service = CategoryService(
        CategoryRepository(db),
    )

    return service.get_all(
       current_user.tenant_id,
        page,
        limit,
        search
    )


@router.put(
    "/{category_id}",
    response_model=CategoryResponse,
)
def update_category(
    category_id: UUID,
    request: UpdateCategoryRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    service = CategoryService(
        CategoryRepository(db),
    )

    category = service.update(
        current_user.tenant_id,
        category_id,
        request,
    )
    db.commit()
    return category


@router.delete(
    "/{category_id}",
)
def delete_category(
    category_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    service = CategoryService(
        CategoryRepository(db),
    )

    category = service.delete(
        current_user.tenant_id,
        category_id,
    )
    db.commit()
    
    return {
        "message": "Category deleted successfully."
    }