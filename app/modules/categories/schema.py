from uuid import UUID

from pydantic import BaseModel


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

    class Config:
        from_attributes = True