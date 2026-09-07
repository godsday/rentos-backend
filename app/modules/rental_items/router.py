import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.modules.rental_items.schema import (
    CreateRentalItemRequest,
    RentalItemResponse,
    UpdateRentalItemRequest,
)
from app.modules.rental_items.service import RentalItemService

router = APIRouter(
    prefix="/rentals/{rental_id}/items",
    tags=["Rental Items"],
)


@router.post(
    "",
    response_model=RentalItemResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_rental_item(
    rental_id: uuid.UUID,
    request: CreateRentalItemRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = RentalItemService(db)

    return service.create(
        current_user.tenant_id,
        rental_id,
        request,
    )


@router.get(
    "",
    response_model=list[RentalItemResponse],
)
def get_rental_items(
    rental_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = RentalItemService(db)

    return service.get_by_rental(
        current_user.tenant_id,
        rental_id,
    )


@router.put(
    "/{rental_item_id}",
    response_model=RentalItemResponse,
)
def update_rental_item(
    rental_id: uuid.UUID,
    rental_item_id: uuid.UUID,
    request: UpdateRentalItemRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = RentalItemService(db)

    return service.update(
        current_user.tenant_id,
        rental_id,
        rental_item_id,
        request,
    )


@router.delete(
    "/{rental_item_id}",
)
def delete_rental_item(
    rental_id: uuid.UUID,
    rental_item_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = RentalItemService(db)

    return service.delete(
        current_user.tenant_id,
        rental_id,
        rental_item_id,
    )
