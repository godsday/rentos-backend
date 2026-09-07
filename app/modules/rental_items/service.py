from decimal import Decimal
import uuid

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.modules.items.repository import ItemRepository
from app.modules.rental_items.models import RentalItem
from app.modules.rental_items.repository import RentalItemRepository
from app.modules.rental_items.schema import (
    CreateRentalItemRequest,
    UpdateRentalItemRequest,
)
from app.modules.rentals.models import Rental, RentalStatus
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
        rental = self._get_draft_rental(tenant_id, rental_id)

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

        if request.quantity <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Quantity must be greater than zero",
            )

        if request.quantity > item.available_quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    f"Only {item.available_quantity} units "
                    "are currently available"
                ),
            )

        existing = self.repository.get_by_rental_and_item(
            rental_id,
            request.item_id,
        )

        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Item already exists in this rental",
            )

        subtotal = Decimal(request.quantity) * item.rental_price
        rental_item = RentalItem(
            rental_id=rental_id,
            item_id=item.id,
            quantity=request.quantity,
            rental_price=item.rental_price,
            subtotal=subtotal,
        )

        item.available_quantity -= request.quantity
        rental_item = self.repository.create(rental_item)
        self._sync_rental_totals(rental)

        return rental_item

    def update(
        self,
        tenant_id: uuid.UUID,
        rental_id: uuid.UUID,
        rental_item_id: uuid.UUID,
        request: UpdateRentalItemRequest,
    ) -> RentalItem:
        rental = self._get_draft_rental(tenant_id, rental_id)

        rental_item = self.repository.get_by_id(rental_item_id)

        if rental_item is None or rental_item.rental_id != rental_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Rental item not found.",
            )

        item = self.item_repository.get_by_id(rental_item.item_id)

        if item is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Item not found.",
            )

        quantity_delta = request.quantity - rental_item.quantity

        if quantity_delta > 0:
            if quantity_delta > item.available_quantity:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=(
                        f"Only {item.available_quantity} units "
                        "are currently available"
                    ),
                )
            item.available_quantity -= quantity_delta
        elif quantity_delta < 0:
            item.available_quantity += abs(quantity_delta)

        rental_item.quantity = request.quantity
        rental_item.subtotal = (
            Decimal(request.quantity) * rental_item.rental_price
        )

        self.item_repository.update(item)
        rental_item = self.repository.update(rental_item)
        self._sync_rental_totals(rental)

        return rental_item

    def delete(
        self,
        tenant_id: uuid.UUID,
        rental_id: uuid.UUID,
        rental_item_id: uuid.UUID,
    ) -> dict:
        rental = self._get_draft_rental(tenant_id, rental_id)

        rental_item = self.repository.get_by_id(rental_item_id)

        if rental_item is None or rental_item.rental_id != rental_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Rental item not found.",
            )

        item = self.item_repository.get_by_id(rental_item.item_id)

        if item is not None:
            item.available_quantity += rental_item.quantity
            self.item_repository.update(item)

        self.repository.soft_delete(rental_item)
        self._sync_rental_totals(rental)

        return {
            "message": "Rental item removed successfully.",
        }

    def get_by_rental(
        self,
        tenant_id: uuid.UUID,
        rental_id: uuid.UUID,
    ) -> list[RentalItem]:
        rental = self.rental_repository.get_by_id_and_tenant(
            tenant_id,
            rental_id,
        )

        if not rental:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Rental not found",
            )

        return self.repository.get_by_rental(rental_id)

    def _get_draft_rental(
        self,
        tenant_id: uuid.UUID,
        rental_id: uuid.UUID,
    ) -> Rental:
        rental = self.rental_repository.get_by_id_and_tenant(
            tenant_id,
            rental_id,
        )

        if not rental:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Rental not found",
            )

        if rental.status != RentalStatus.DRAFT:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Rental items can only be modified on a draft rental",
            )

        return rental

    def _sync_rental_totals(self, rental: Rental) -> None:
        rental.total_amount = self.repository.get_total_by_rental(
            rental.id,
        )
        rental.remaining_amount = (
            rental.total_amount - rental.initial_payment
        )
        self.rental_repository.update(rental)
