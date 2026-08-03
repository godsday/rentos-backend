from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config.settings import settings

DATABASE_URL = (
    f"postgresql+psycopg2://"
    f"{settings.database_user}:"
    f"{settings.database_password}@"
    f"{settings.database_host}:"
    f"{settings.database_port}/"
    f"{settings.database_name}"
)

engine = create_engine(
    DATABASE_URL,
    echo=settings.debug,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)
from sqlalchemy.orm import Session


def get_db():
    db: Session = SessionLocal()

    try:
        yield db
        db.commit()        # Commit if everything succeeded
    except Exception:
        db.rollback()      # Rollback on any exception
        raise
    finally:
        db.close()