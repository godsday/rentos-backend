"""create rentals table

Revision ID: 63142073771f
Revises: fca9366aeaa9
Create Date: 2026-08-16 20:31:59.441518

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "63142073771f"
down_revision: Union[str, Sequence[str], None] = "fca9366aeaa9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass