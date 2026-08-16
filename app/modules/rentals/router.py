from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.modules.customers.repository import CustomerRepository
from app.modules.rentals.repository import RentalRepository
from app.modules.rentals.schema import (
    CreateRentalRequest,
    RentalResponse,
    UpdateRentalRequest,
)
from app.modules.rentals.service import RentalService


router = APIRouter(
    prefix="/rentals",
    tags=["Rentals"],
)


def get_rental_service(
    db: Session = Depends(get_db),
):
    """
    Create RentalService with its repositories.
    """

    rental_repository = RentalRepository(db)

    customer_repository = CustomerRepository(db)

    return RentalService(
        rental_repository,
        customer_repository,
    )


@router.post(
    "",
    response_model=RentalResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_rental(
    request: CreateRentalRequest,
    current_user=Depends(get_current_user),
    service: RentalService = Depends(get_rental_service),
):
    """
    Create a new rental.
    """

    return service.create(
        current_user.tenant_id,
        request,
    )


@router.get(
    "",
    response_model=list[RentalResponse],
)
def get_rentals(
    page: int = Query(
        default=1,
        ge=1,
    ),
    limit: int = Query(
        default=20,
        ge=1,
        le=100,
    ),
    current_user=Depends(get_current_user),
    service: RentalService = Depends(get_rental_service),
):
    """
    Get paginated rentals for the current tenant.
    """

    return service.get_all(
        current_user.tenant_id,
        page,
        limit,
    )


@router.get(
    "/{rental_id}",
    response_model=RentalResponse,
)
def get_rental(
    rental_id: UUID,
    current_user=Depends(get_current_user),
    service: RentalService = Depends(get_rental_service),
):
    """
    Get a single rental.
    """

    return service.get_by_id(
        current_user.tenant_id,
        rental_id,
    )


@router.put(
    "/{rental_id}",
    response_model=RentalResponse,
)
def update_rental(
    rental_id: UUID,
    request: UpdateRentalRequest,
    current_user=Depends(get_current_user),
    service: RentalService = Depends(get_rental_service),
):
    """
    Update a rental.
    """

    return service.update(
        current_user.tenant_id,
        rental_id,
        request,
    )


@router.delete(
    "/{rental_id}",
)
def delete_rental(
    rental_id: UUID,
    current_user=Depends(get_current_user),
    service: RentalService = Depends(get_rental_service),
):
    """
    Soft delete a rental.
    """

    return service.delete(
        current_user.tenant_id,
        rental_id,
    )