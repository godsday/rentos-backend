from fastapi import APIRouter

from app.api.v1.health import router as health_router
from app.api.v1.test_db import router as test_db_router
from app.modules.auth.router import router as users_router
from app.modules.categories.router import router as category_router
from app.modules.items.router import router as items_router
from app.modules.customers.router import router as customers_router



api_router = APIRouter()

api_router.include_router(users_router, tags=["Users"])
api_router.include_router(category_router)
api_router.include_router(items_router)
api_router.include_router(customers_router)