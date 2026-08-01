from app.db.base_repository import BaseRepository
from app.modules.roles.models import Role


class RoleRepository(BaseRepository[Role]):
    model = Role

    def __init__(self, db):
        super().__init__(db, Role)

    def get_by_name(self, name: str):
        return (
            self.db.query(Role)
            .filter(
                Role.name == name,
                Role.is_deleted.is_(False),
            )
            .first()
        )