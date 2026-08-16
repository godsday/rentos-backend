from fastapi import HTTPException, status

from app.modules.customers.models import Customer
from app.modules.customers.repository import CustomerRepository
from app.modules.customers.schema import (
    CreateCustomerRequest,
    UpdateCustomerRequest,
)


class CustomerService:
    """
    Business logic for Customer Management.
    """

    def __init__(
        self,
        repository: CustomerRepository,
    ):
        self.repository = repository

    @staticmethod
    def normalize_phone(phone: str) -> str:
        """
        Normalize phone number before storing/searching.

        Keeps only digits.
        Example:
        +91 98765-43210 -> 919876543210
        """
        return "".join(
            character
            for character in phone
            if character.isdigit()
        )

    def create(
        self,
        tenant_id,
        request: CreateCustomerRequest,
    ):
        phone = self.normalize_phone(request.phone)

        existing_customer = self.repository.get_by_phone(
            tenant_id,
            phone,
        )

        if existing_customer:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Customer with this phone number already exists.",
            )

        customer = Customer(
            tenant_id=tenant_id,
            full_name=request.full_name,
            phone=phone,
            email=request.email,
            address=request.address,
            city=request.city,
            state=request.state,
            country=request.country,
            pincode=request.pincode,
            notes=request.notes,
            is_active=True,
        )

        return self.repository.create(customer)

    def get_by_id(
        self,
        tenant_id,
        customer_id,
    ):
        customer = self.repository.get_by_id_and_tenant(
            tenant_id,
            customer_id,
        )

        if customer is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found.",
            )

        return customer

    def get_all(
        self,
        tenant_id,
        page,
        limit,
        search=None,
        is_active=None,
        sort_by="full_name",
        sort_order="asc",
    ):
        customers, total = self.repository.get_all_by_tenant(
            tenant_id=tenant_id,
            page=page,
            limit=limit,
            search=search,
            is_active=is_active,
            sort_by=sort_by,
            sort_order=sort_order,
        )

        return {
            "items": customers,
            "total": total,
            "page": page,
            "limit": limit,
            "total_pages": (
                (total + limit - 1) // limit
                if total > 0
                else 0
            ),
        }

    def update(
        self,
        tenant_id,
        customer_id,
        request: UpdateCustomerRequest,
    ):
        customer = self.repository.get_by_id_and_tenant(
            tenant_id,
            customer_id,
        )

        if customer is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found.",
            )

        phone = self.normalize_phone(request.phone)

        existing_customer = self.repository.get_by_phone(
            tenant_id,
            phone,
        )

        if (
            existing_customer
            and existing_customer.id != customer.id
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Customer with this phone number already exists.",
            )

        customer.full_name = request.full_name
        customer.phone = phone
        customer.email = request.email
        customer.address = request.address
        customer.city = request.city
        customer.state = request.state
        customer.country = request.country
        customer.pincode = request.pincode
        customer.notes = request.notes
        customer.is_active = request.is_active

        return self.repository.update(customer)

    def delete(
        self,
        tenant_id,
        customer_id,
    ):
        customer = self.repository.get_by_id_and_tenant(
            tenant_id,
            customer_id,
        )

        if customer is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found.",
            )

        self.repository.soft_delete(customer)

        return {
            "message": "Customer deleted successfully."
        }