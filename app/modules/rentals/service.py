from uuid import UUID

from fastapi import HTTPException, status

from app.modules.customers.repository import CustomerRepository
from app.modules.items.repository import ItemRepository
from app.modules.rental_items.repository import RentalItemRepository
from app.modules.rentals.models import Rental, RentalStatus
from app.modules.rentals.repository import RentalRepository
from app.modules.rentals.schema import (
    ActivateRentalRequest,
    CreateRentalRequest,
    UpdateRentalRequest,
)


class RentalService:
    """
    Business logic for Rental Management.
    """

    def __init__(
        self,
        repository: RentalRepository,
        customer_repository: CustomerRepository,
        rental_item_repository: RentalItemRepository,
        item_repository: ItemRepository,
    ):
        self.repository = repository
        self.customer_repository = customer_repository
        self.rental_item_repository = rental_item_repository
        self.item_repository = item_repository

    def create(
        self,
        tenant_id: UUID,
        request: CreateRentalRequest,
    ):
        customer = self.customer_repository.get_by_id(
            request.customer_id,
        )

        if customer is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found.",
            )

        if customer.tenant_id != tenant_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied.",
            )

        if request.expected_return_date < request.rental_date:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Expected return date cannot be before rental date.",
            )

        rental = Rental(
            tenant_id=tenant_id,
            customer_id=request.customer_id,
            rental_date=request.rental_date,
            expected_return_date=request.expected_return_date,
            status=RentalStatus.DRAFT,
            total_amount=0,
            notes=request.notes,
        )

        return self.repository.create(rental)

    def get_by_id(
        self,
        tenant_id: UUID,
        rental_id: UUID,
    ):
        rental = self.repository.get_by_id_and_tenant(
            tenant_id,
            rental_id,
        )

        if rental is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Rental not found.",
            )

        return rental

    def get_all(
        self,
        tenant_id: UUID,
        page: int,
        limit: int,
    ):
        return self.repository.get_all_by_tenant(
            tenant_id,
            page,
            limit,
        )

    def get_by_customer(
        self,
        tenant_id: UUID,
        customer_id: UUID,
    ):
        customer = self.customer_repository.get_by_id(
            customer_id,
        )

        if customer is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found.",
            )

        if customer.tenant_id != tenant_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied.",
            )

        return self.repository.get_by_customer(
            tenant_id,
            customer_id,
        )

    def update(
        self,
        tenant_id: UUID,
        rental_id: UUID,
        request: UpdateRentalRequest,
    ):
        rental = self.get_by_id(
            tenant_id,
            rental_id,
        )

        if rental.status == RentalStatus.COMPLETED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Completed rental cannot be updated.",
            )

        if request.expected_return_date is not None:
            if request.expected_return_date < rental.rental_date:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Expected return date cannot be before rental date.",
                )

            rental.expected_return_date = request.expected_return_date

        if request.notes is not None:
            rental.notes = request.notes

        return self.repository.update(rental)

    def delete(
        self,
        tenant_id: UUID,
        rental_id: UUID,
    ):
        rental = self.get_by_id(
            tenant_id,
            rental_id,
        )

        if rental.status != RentalStatus.DRAFT:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only draft rentals can be deleted.",
            )

        self._restore_inventory_for_rental(rental_id)
        self.repository.soft_delete(rental)

        return {
            "message": "Rental deleted successfully.",
        }

    def activate(
        self,
        tenant_id: UUID,
        rental_id: UUID,
        request: ActivateRentalRequest,
    ):
        rental = self.get_by_id(
            tenant_id,
            rental_id,
        )

        if rental.status != RentalStatus.DRAFT:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only draft rentals can be activated.",
            )

        rental_items = self.rental_item_repository.get_by_rental(
            rental_id,
        )

        if not rental_items:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Rental must have at least one item before activation.",
            )

        if request.initial_payment > rental.total_amount:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Initial payment cannot exceed total amount.",
            )

        rental.initial_payment = request.initial_payment
        rental.remaining_amount = (
            rental.total_amount - request.initial_payment
        )
        rental.status = RentalStatus.ACTIVE

        return self.repository.update(rental)

    def recalculate_total(self, rental_id: UUID) -> Rental:
        rental = self.repository.get_by_id(rental_id)

        if rental is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Rental not found.",
            )

        rental.total_amount = (
            self.rental_item_repository.get_total_by_rental(rental_id)
        )
        rental.remaining_amount = (
            rental.total_amount - rental.initial_payment
        )

        return self.repository.update(rental)

    def _restore_inventory_for_rental(
        self,
        rental_id: UUID,
    ) -> None:
        rental_items = self.rental_item_repository.get_by_rental(
            rental_id,
        )

        for rental_item in rental_items:
            item = self.item_repository.get_by_id(
                rental_item.item_id,
            )

            if item is not None:
                item.available_quantity += rental_item.quantity
                self.item_repository.update(item)

            self.rental_item_repository.soft_delete(rental_item)
