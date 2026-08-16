"""create customers table

Revision ID: d615ce9ed3c1
Revises: 67383637f68d
Create Date: 2026-08-16 06:17:29.383008

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d615ce9ed3c1"
down_revision: Union[str, Sequence[str], None] = "67383637f68d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table(
        "customers",
        sa.Column("tenant_id", sa.UUID(), nullable=False),
        sa.Column(
            "full_name",
            sa.String(length=150),
            nullable=False,
        ),
        sa.Column(
            "phone",
            sa.String(length=20),
            nullable=False,
        ),
        sa.Column(
            "email",
            sa.String(length=255),
            nullable=True,
        ),
        sa.Column(
            "address",
            sa.String(length=500),
            nullable=True,
        ),
        sa.Column(
            "city",
            sa.String(length=100),
            nullable=True,
        ),
        sa.Column(
            "state",
            sa.String(length=100),
            nullable=True,
        ),
        sa.Column(
            "country",
            sa.String(length=100),
            nullable=True,
        ),
        sa.Column(
            "pincode",
            sa.String(length=10),
            nullable=True,
        ),
        sa.Column(
            "notes",
            sa.String(length=1000),
            nullable=True,
        ),
        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
        ),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "is_deleted",
            sa.Boolean(),
            nullable=False,
        ),
        sa.Column(
            "deleted_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["tenant_id"],
            ["tenants.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "tenant_id",
            "phone",
            name="uq_customer_tenant_phone",
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_table("customers")