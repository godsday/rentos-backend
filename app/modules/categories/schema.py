from uuid import UUID

from pydantic import BaseModel, ConfigDict


class CreateCategoryRequest(BaseModel):
    name: str
    description: str | None = None


class UpdateCategoryRequest(BaseModel):
    name: str
    description: str | None = None


class CategoryResponse(BaseModel):
    id: UUID
    name: str
    description: str | None

    model_config = ConfigDict(
        from_attributes=True,
    )