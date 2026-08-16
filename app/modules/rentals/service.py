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
        """
        Create a new rental for a tenant.
        """

        # Make sure the customer belongs to this tenant.
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
                detail="Customer does not belong to this tenant.",
            )

        rental = Rental(
            tenant_id=tenant_id,
            customer_id=request.customer_id,
            rental_date=request.rental_date,
            expected_return_date=request.expected_return_date,
            security_deposit=request.security_deposit,
            total_amount=0,
            status=RentalStatus.PENDING,
            notes=request.notes,
        )

        return self.repository.create(rental)

    def get_all(
        self,
        tenant_id: UUID,
        page: int,
        limit: int,
    ):
        """
        Return all rentals belonging to the tenant.
        """

        return self.repository.get_all_by_tenant(
            tenant_id,
            page,
            limit,
        )

    def get_by_id(
        self,
        tenant_id: UUID,
        rental_id: UUID,
    ):
        """
        Return one rental belonging to the tenant.
        """

        rental = self.repository.get_by_id_and_tenant(
            rental_id,
            tenant_id,
        )

        if rental is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Rental not found.",
            )

        return rental

    def update(
        self,
        tenant_id: UUID,
        rental_id: UUID,
        request: UpdateRentalRequest,
    ):
        """
        Update an existing rental.
        """

        rental = self.repository.get_by_id_and_tenant(
            rental_id,
            tenant_id,
        )

        if rental is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Rental not found.",
            )

        if request.expected_return_date is not None:
            if request.expected_return_date < rental.rental_date:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=(
                        "Expected return date cannot be "
                        "before rental date."
                    ),
                )

            rental.expected_return_date = (
                request.expected_return_date
            )

        if request.actual_return_date is not None:
            rental.actual_return_date = (
                request.actual_return_date
            )

        if request.security_deposit is not None:
            rental.security_deposit = (
                request.security_deposit
            )

        if request.status is not None:
            rental.status = request.status

        if request.notes is not None:
            rental.notes = request.notes

        return self.repository.update(rental)

    def delete(
        self,
        tenant_id: UUID,
        rental_id: UUID,
    ):
        """
        Soft delete a rental.
        """

        rental = self.repository.get_by_id_and_tenant(
            rental_id,
            tenant_id,
        )

        if rental is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Rental not found.",
            )

        self.repository.soft_delete(rental)

        return {
            "message": "Rental deleted successfully.",
        }