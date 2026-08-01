from sqlalchemy.orm import Session

from app.db.base_repository import BaseRepository
from app.modules.auth.models import User
from uuid import UUID


class UserRepository(BaseRepository[User]):
    
    def __init__(self, db: Session):
        super().__init__(db, User)

    def get_by_email(self, email: str) -> User | None:
        return (
            self.db.query(User)
            .filter(
                User.email == email,
                User.is_deleted.is_(False),
            )
            .first()
        )

    def get_by_phone(self, phone: str) -> User | None:
        return (
            self.db.query(User)
            .filter(
                User.phone == phone,
                User.is_deleted.is_(False),
            )
            .first()
        )

    def get_by_id(self, user_id: UUID) -> User | None:
        return (
            self.db.query(User)
            .filter(
                User.id == user_id,
                User.is_deleted.is_(False),
            )
            .first()
        )
