from fastapi import HTTPException, status

from app.modules.categories.repository import CategoryRepository
from app.modules.items.models import Item
from app.modules.items.repository import ItemRepository
from app.modules.items.schema import (
    CreateItemRequest,
    UpdateItemRequest,
)


class ItemService:
    """
    Business logic for Item Management.
    """

    def __init__(self, repository: ItemRepository):
        self.repository = repository

    def create(
        self,
        tenant_id,
        request: CreateItemRequest

):
    # Category Repository
        category_repository = CategoryRepository(
     self.repository.db,
     
)
    # Verify Category Exists
        category = category_repository.get_by_id(
            request.category_id,
        )
        
        if category is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found.",
            )

    # Verify Category belongs to current Tenant
        if category.tenant_id != tenant_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied.",
            )

         # Check duplicate Item Name
        if self.repository.get_by_name(
            tenant_id,
            request.name,
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Item name already exists.",
            )

   # Check duplicate SKU
        if self.repository.get_by_sku(
            tenant_id,
            request.sku,
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="SKU already exists.",
            )

# Before creating an item, validate the SKU.
        if self.repository.get_by_sku(
            tenant_id,
            request.sku,
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="SKU already exists.",
            )
            

    # Create Item
        item = Item(
            tenant_id=tenant_id,
            category_id=request.category_id,
            name=request.name,
            sku=request.sku,
            description=request.description,
            rental_price=request.rental_price,
            security_deposit=request.security_deposit,
            quantity=request.quantity,
            available_quantity=request.quantity,
            barcode=request.barcode,
            image=request.image,
            is_active=True,
        )

        return self.repository.create(item)

    def get_all(
        self,
        tenant_id,
        page:int,
        limit:int, 
        search=None   
       
    ):
        return self.repository.get_all_by_tenant(
            tenant_id,
            page,
            limit,
            search
            

    )

    def update(
        self,
        tenant_id,
        item_id,
        request: UpdateItemRequest,
    ):
        # Find Item
        item = self.repository.get_by_id(
            item_id,
        )

        if item is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Item not found.",
            )

        # Verify Tenant Access
        if item.tenant_id != tenant_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied.",
            )

        # Verify Category Exists
        category_repository = CategoryRepository(
            self.repository.db,
        )

        category = category_repository.get_by_id(
            request.category_id,
        )

        if category is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found.",
            )

        # Verify Category belongs to Tenant
        if category.tenant_id != tenant_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied.",
            )

        # Check duplicate Name
        existing_item = self.repository.get_by_name(
            tenant_id,
            request.name,
        )

        if (
            existing_item is not None
            and existing_item.id != item.id
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Item name already exists.",
            )

        # Check duplicate SKU
        existing_sku = self.repository.get_by_sku(
            tenant_id,
            request.sku,
        )

        if (
            existing_sku is not None
            and existing_sku.id != item.id
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="SKU already exists.",
            )

        # Update Item
        item.category_id = request.category_id
        item.name = request.name
        item.sku = request.sku
        item.description = request.description
        item.rental_price = request.rental_price
        item.security_deposit = request.security_deposit

        # Update Quantity
        item.quantity = request.quantity
        item.available_quantity = request.quantity

        item.barcode = request.barcode
        item.image = request.image
        item.is_active = request.is_active

        return self.repository.update(item)

    def delete(
        self,
        tenant_id,
        item_id,
    ):
        # Find Item
        item = self.repository.get_by_id(
            item_id,
        )

        if item is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Item not found.",
            )

        # Verify Tenant Access
        if item.tenant_id != tenant_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied.",
            )

        # Soft Delete
        self.repository.soft_delete(
            item,
        )