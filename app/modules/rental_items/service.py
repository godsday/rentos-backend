from decimal import Decimal
import uuid

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.modules.items.repository import ItemRepository
from app.modules.rental_items.models import RentalItem
from app.modules.rental_items.repository import RentalItemRepository
from app.modules.rental_items.schema import CreateRentalItemRequest
from app.modules.rentals.repository import RentalRepository


class RentalItemService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = RentalItemRepository(db)
        self.rental_repository = RentalRepository(db)
        self.item_repository = ItemRepository(db)

    def create(
        self,
        tenant_id: uuid.UUID,
        rental_id: uuid.UUID,
        request: CreateRentalItemRequest,
    ) -> RentalItem:

        # 1. Validate rental
        rental = self.rental_repository.get_by_id(
                tenant_id,
                rental_id,
            )
        if not rental:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Rental not found",
            )

        if rental.tenant_id != tenant_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Rental does not belong to this tenant",
            )

        # Only draft rentals can be modified
        if rental.status.value != "DRAFT":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Rental items can only be added to a draft rental",
            )

        # 2. Validate item
        item = self.item_repository.get_by_id(request.item_id)

        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Item not found",
            )

        if item.tenant_id != tenant_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Item does not belong to this tenant",
            )

        if not item.is_active or item.is_deleted:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Item is not active",
            )
          # 3. Validate quantity
        if request.quantity <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Quantity must be greater than zero",
            )

        # 3. Check inventory
        if request.quantity > item.available_quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    f"Only {item.available_quantity} units "
                    "are currently available"
                ),
            )

        # 4. Prevent duplicate item
        existing = self.repository.get_by_rental_and_item(
            rental_id,
            request.item_id,
        )

        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Item already exists in this rental",
                
            )

     # 5. Snapshot current rental price
        rental_price = item.rental_price

        
        subtotal = (
            Decimal(request.quantity) * rental_price
        )
        rental_item = RentalItem(
            rental_id=rental_id,
            item_id=item.id,
            quantity=request.quantity,         
            rental_price=item.rental_price,   
            subtotal=subtotal,
        )

    # 6. Update inventory
        item.available_quantity -= request.quantity

    # 7. Create rental item
        rental_item = self.repository.create(rental_item)

    # 8. Recalculate rental total
        rental.total_amount = (
            self.repository.get_total_by_rental(rental_id)
        )

    # 9. Recalculate remaining amount
        rental.remaining_amount = (
            rental.total_amount - rental.initial_payment
        )    

        self.rental_repository.update(rental)

        return rental_item


    def get_by_rental(
        self,
        tenant_id: uuid.UUID,
        rental_id: uuid.UUID,
    ) -> list[RentalItem]:

        rental = self.rental_repository.get_by_id(tenant_id, rental_id,)

        if not rental:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Rental not found",
            )

        if rental.tenant_id != tenant_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Rental does not belong to this tenant",
            )

        return self.repository.get_by_rental(rental_id)