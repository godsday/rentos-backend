from fastapi import FastAPI

from app.config.settings import settings
from app.api.v1.router import api_router
from app.common.exceptions.handlers import register_exception_handlers
from app.db.session import SessionLocal
from app.common.seeders.role_seeder import seed_roles

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)

register_exception_handlers(app)
app.include_router(api_router, prefix="/api/v1")


@app.on_event("startup")
def startup():
    db = SessionLocal()

    try:
        seed_roles(db)
    finally:
        db.close()


@app.get("/")
async def root():
    return {
        "status": "success",
        "message": f"Welcome to {settings.app_name} 🚀",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }