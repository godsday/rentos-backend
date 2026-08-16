from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.modules.customers.repository import CustomerRepository
from app.modules.customers.schema import (
    CreateCustomerRequest,
    CustomerListResponse,
    CustomerResponse,
    UpdateCustomerRequest,
)
from app.modules.customers.service import CustomerService


router = APIRouter(
    prefix="/customers",
    tags=["Customers"],
)


def get_customer_service(
    db: Session = Depends(get_db),
):
    repository = CustomerRepository(db)

    return CustomerService(repository)


@router.post(
    "",
    response_model=CustomerResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_customer(
    request: CreateCustomerRequest,
    current_user=Depends(get_current_user),
    service: CustomerService = Depends(get_customer_service),
):
    return service.create(
        current_user.tenant_id,
        request,
    )


@router.get(
    "",
    response_model=CustomerListResponse,
)
def get_customers(
    page: int = Query(
        default=1,
        ge=1,
    ),
    limit: int = Query(
        default=20,
        ge=1,
        le=100,
    ),
    search: str | None = Query(
        default=None,
    ),
    is_active: bool | None = Query(
        default=None,
    ),
    sort_by: str = Query(
        default="full_name",
        pattern="^(full_name|phone|email|created_at|updated_at)$",
    ),
    sort_order: str = Query(
        default="asc",
        pattern="^(asc|desc)$",
    ),
    current_user=Depends(get_current_user),
    service: CustomerService = Depends(get_customer_service),
):
    return service.get_all(
        current_user.tenant_id,
        page,
        limit,
        search,
        is_active,
        sort_by,
        sort_order,
    )


@router.get(
    "/{customer_id}",
    response_model=CustomerResponse,
)
def get_customer(
    customer_id: UUID,
    current_user=Depends(get_current_user),
    service: CustomerService = Depends(get_customer_service),
):
    return service.get_by_id(
        current_user.tenant_id,
        customer_id,
    )


@router.put(
    "/{customer_id}",
    response_model=CustomerResponse,
)
def update_customer(
    customer_id: UUID,
    request: UpdateCustomerRequest,
    current_user=Depends(get_current_user),
    service: CustomerService = Depends(get_customer_service),
):
    return service.update(
        current_user.tenant_id,
        customer_id,
        request,
    )


@router.delete(
    "/{customer_id}",
)
def delete_customer(
    customer_id: UUID,
    current_user=Depends(get_current_user),
    service: CustomerService = Depends(get_customer_service),
):
    return service.delete(
        current_user.tenant_id,
        customer_id,
    )