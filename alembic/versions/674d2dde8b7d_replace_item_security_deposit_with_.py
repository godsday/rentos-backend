"""replace item security deposit with purchase price and enforce unique name

Revision ID: 674d2dde8b7d
Revises: 0d6d7bdff714
Create Date: 2026-08-20 12:02:40.932645

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "8a1234567890"
down_revision: Union[str, Sequence[str], None] = "0d6d7bdff714"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # Add purchase price.
    op.add_column(
        "items",
        sa.Column(
            "purchase_price",
            sa.Numeric(precision=10, scale=2),
            nullable=False,
        ),
    )

    # Remove security deposit from item.
    op.drop_column(
        "items",
        "security_deposit",
    )

    # Item names must be unique within a tenant.
    op.create_unique_constraint(
        "uq_item_tenant_name",
        "items",
        ["tenant_id", "name"],
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_constraint(
        "uq_item_tenant_name",
        "items",
        type_="unique",
    )

    op.add_column(
        "items",
        sa.Column(
            "security_deposit",
            sa.Numeric(precision=10, scale=2),
            nullable=False,
            server_default="0",
        ),
    )

    op.drop_column(
        "items",
        "purchase_price",
    )