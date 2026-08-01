from sqlalchemy.orm import Session

from app.modules.roles.models import Role


DEFAULT_ROLES = [
    {
        "name": "SUPER_ADMIN",
        "description": "Platform Administrator",
    },
    {
        "name": "TENANT_OWNER",
        "description": "Business Owner",
    },
    {
        "name": "MANAGER",
        "description": "Business Manager",
    },
    {
        "name": "STAFF",
        "description": "Staff Member",
    },
]


def seed_roles(db: Session):
    for role in DEFAULT_ROLES:
        exists = (
            db.query(Role)
            .filter(Role.name == role["name"])
            .first()
        )

        if exists:
            continue

        db.add(Role(**role))

    db.commit()