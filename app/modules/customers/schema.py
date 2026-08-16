from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class CreateCustomerRequest(BaseModel):
    full_name: str = Field(
        ...,
        min_length=2,
        max_length=150,
    )

    phone: str = Field(
        ...,
        min_length=7,
        max_length=20,
    )

    email: EmailStr | None = None

    address: str | None = Field(
        default=None,
        max_length=500,
    )

    city: str | None = Field(
        default=None,
        max_length=100,
    )

    state: str | None = Field(
        default=None,
        max_length=100,
    )

    country: str | None = Field(
        default=None,
        max_length=100,
    )

    pincode: str | None = Field(
        default=None,
        max_length=10,
    )

    notes: str | None = Field(
        default=None,
        max_length=1000,
    )


class UpdateCustomerRequest(BaseModel):
    full_name: str = Field(
        ...,
        min_length=2,
        max_length=150,
    )

    phone: str = Field(
        ...,
        min_length=7,
        max_length=20,
    )

    email: EmailStr | None = None

    address: str | None = Field(
        default=None,
        max_length=500,
    )

    city: str | None = Field(
        default=None,
        max_length=100,
    )

    state: str | None = Field(
        default=None,
        max_length=100,
    )

    country: str | None = Field(
        default=None,
        max_length=100,
    )

    pincode: str | None = Field(
        default=None,
        max_length=10,
    )

    notes: str | None = Field(
        default=None,
        max_length=1000,
    )

    is_active: bool = True


class CustomerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    tenant_id: UUID
    full_name: str
    phone: str
    email: EmailStr | None
    address: str | None
    city: str | None
    state: str | None
    country: str | None
    pincode: str | None
    notes: str | None
    is_active: bool


class CustomerListResponse(BaseModel):
    items: list[CustomerResponse]
    total: int
    page: int
    limit: int
    total_pages: int