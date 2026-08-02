from fastapi import HTTPException, status

from app.modules.categories.models import Category
from app.modules.categories.repository import CategoryRepository
from app.modules.categories.schema import (
    CreateCategoryRequest,
    UpdateCategoryRequest,
)


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

    def get_all(self, tenant_id):
        return self.repository.get_all_by_tenant(
            tenant_id,
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

        self.repository.soft_delete(category)