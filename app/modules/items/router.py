from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.modules.auth.models import User
from app.modules.items.repository import ItemRepository
from app.modules.items.schema import (
    CreateItemRequest,
    ItemResponse,
    UpdateItemRequest,
)
from app.modules.items.service import ItemService

router = APIRouter(
    prefix="/items",
    tags=["Items"],
)


@router.post(
    "",
    response_model=ItemResponse,
)
def create_item(
    request: CreateItemRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repository = ItemRepository(db)

    service = ItemService(repository)

    return service.create(
        current_user.tenant_id,
        request,
    )


@router.get(
    "",
    response_model=list[ItemResponse],
)
def get_items(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    search: str | None = Query(None)
):
    repository = ItemRepository(db)

    service = ItemService(repository)

    return service.get_all(
        current_user.tenant_id,
        page,
        limit,
        search
    )


@router.put(
    "/{item_id}",
    response_model=ItemResponse,
)
def update_item(
    item_id: UUID,
    request: UpdateItemRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repository = ItemRepository(db)

    service = ItemService(repository)

    return service.update(
        current_user.tenant_id,
        item_id,
        request,
    )


@router.delete(
    "/{item_id}",
)
def delete_item(
    item_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repository = ItemRepository(db)

    service = ItemService(repository)

    service.delete(
        current_user.tenant_id,
        item_id,
    )

    return {
        "message": "Item deleted successfully."
    }