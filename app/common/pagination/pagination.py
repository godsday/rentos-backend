from pydantic import BaseModel


class PaginationParams(BaseModel):
    page: int = 1
    limit: int = 20