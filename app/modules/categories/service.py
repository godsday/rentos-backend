from fastapi import HTTPException, status

from app.modules.categories.models import Category
from app.modules.categories.repository import CategoryRepository
from app.modules.categories.schema import (
    CreateCategoryRequest,
    UpdateCategoryRequest,
)
from app.modules.items.repository import ItemRepository



class CategoryService:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    def create(self, tenant_id, request: CreateCategoryRequest):

        if self.repository.get_by_name(
            tenant_id,
            request.name,
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category already exists.",
            )

        return self.repository.create(
            Category(
                tenant_id=tenant_id,
                name=request.name,
                description=request.description,
            )
        )

    def get_all(self, tenant_id, page :int , limit :int, search=None, sort="name"):
        return self.repository.get_all_by_tenant(
            tenant_id,
            page,
            limit,
            search,
            sort,                
        )

    def update(
        self,
        tenant_id,
        category_id,
        request: UpdateCategoryRequest,
    ):

        category = self.repository.get_by_id(
            category_id,
        )

        if category is None:
            raise HTTPException(
                status_code=404,
                detail="Category not found.",
            )

        if category.tenant_id != tenant_id:
            raise HTTPException(
                status_code=403,
                detail="Access denied.",
            )

        category.name = request.name
        category.description = request.description

        return self.repository.update(category)

    def delete(
        self,
        tenant_id,
        category_id,
    ):

        category = self.repository.get_by_id(
            category_id,
        )

        if category is None:
            raise HTTPException(
                status_code=404,
                detail="Category not found.",
            )

        if category.tenant_id != tenant_id:
            raise HTTPException(
                status_code=403,
                detail="Access denied.",
            )
        item_repository = ItemRepository(
            self.repository.db,
        )

        if item_repository.has_items(
            tenant_id,
            category.id,
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "Cannot delete category. "
                    "Items exist under this category."
                ),
            )

        self.repository.soft_delete(category)