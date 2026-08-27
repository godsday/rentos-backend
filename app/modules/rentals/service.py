from datetime import date
from uuid import UUID

from fastapi import HTTPException, status

from app.modules.customers.repository import CustomerRepository
from app.modules.rentals.models import Rental, RentalStatus
from app.modules.rentals.repository import RentalRepository
from app.modules.rentals.schema import (
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
    ):
        self.repository = repository
        self.customer_repository = customer_repository

    def create(
        self,
        tenant_id: UUID,
        request: CreateRentalRequest,
    ):
        # Validate customer
        customer = self.customer_repository.get_by_id(
            request.customer_id,
        )

        if customer is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found.",
            )

        # Prevent cross-tenant access
        if customer.tenant_id != tenant_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied.",
            )

        # Validate dates
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
        rental = self.repository.get_by_id(rental_id)

        if rental is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Rental not found.",
            )

        if rental.tenant_id != tenant_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied.",
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

        # if request.total_amount is not None:
        #     rental.total_amount = request.total_amount

       

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

        self.repository.soft_delete(rental)

        return {
            "message": "Rental deleted successfully.",
        }

    def recalculate_total(self, rental_id: UUID) -> Rental:
        rental = self.repository.get_by_id(rental_id)

        if rental is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Rental not found.",
            )

        rental.total_amount = sum(
            item.subtotal
            for item in rental.items
            if not item.is_deleted
        )

        return self.repository.update(rental)