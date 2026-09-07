from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.modules.customers.repository import CustomerRepository
from app.modules.items.repository import ItemRepository
from app.modules.rental_items.repository import RentalItemRepository
from app.modules.rentals.repository import RentalRepository
from app.modules.rentals.schema import (
    ActivateRentalRequest,
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
) -> RentalService:
    return RentalService(
        repository=RentalRepository(db),
        customer_repository=CustomerRepository(db),
        rental_item_repository=RentalItemRepository(db),
        item_repository=ItemRepository(db),
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
    return service.create(
        current_user.tenant_id,
        request,
    )


@router.get(
    "",
    response_model=list[RentalResponse],
)
def get_rentals(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    current_user=Depends(get_current_user),
    service: RentalService = Depends(get_rental_service),
):
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
    return service.get_by_id(
        current_user.tenant_id,
        rental_id,
    )


@router.get(
    "/customer/{customer_id}",
    response_model=list[RentalResponse],
)
def get_customer_rentals(
    customer_id: UUID,
    current_user=Depends(get_current_user),
    service: RentalService = Depends(get_rental_service),
):
    return service.get_by_customer(
        current_user.tenant_id,
        customer_id,
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
    return service.delete(
        current_user.tenant_id,
        rental_id,
    )


@router.post(
    "/{rental_id}/activate",
    response_model=RentalResponse,
)
def activate_rental(
    rental_id: UUID,
    request: ActivateRentalRequest,
    current_user=Depends(get_current_user),
    service: RentalService = Depends(get_rental_service),
):
    return service.activate(
        current_user.tenant_id,
        rental_id,
        request,
    )