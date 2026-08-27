"""align rental status enum

Revision ID: 0d6d7bdff714
Revises: 63142073771f
Create Date: 2026-08-16
"""

from typing import Sequence, Union

from alembic import op


revision: str = "0d6d7bdff714"
down_revision: Union[str, Sequence[str], None] = "63142073771f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Rename the existing enum
    op.execute(
        """
        ALTER TYPE rental_status
        RENAME TO rental_status_old
        """
    )

    # Create the new enum matching the Python model
    op.execute(
        """
        CREATE TYPE rental_status AS ENUM (
            'DRAFT',
            'ACTIVE',
            'PARTIALLY_RETURNED',
            'COMPLETED',
            'CANCELLED',
            'OVERDUE'
        )
        """
    )

    # Convert existing values to the new enum
    #
    # PENDING  -> DRAFT
    # RETURNED -> COMPLETED
    #
    # ACTIVE and CANCELLED remain unchanged.
    op.execute(
        """
        ALTER TABLE rentals
        ALTER COLUMN status TYPE rental_status
        USING (
            CASE status::text
                WHEN 'PENDING' THEN 'DRAFT'
                WHEN 'RETURNED' THEN 'COMPLETED'
                ELSE status::text
            END
        )::rental_status
        """
    )

    # Remove the old enum
    op.execute(
        """
        DROP TYPE rental_status_old
        """
    )


def downgrade() -> None:
    # Rename current enum
    op.execute(
        """
        ALTER TYPE rental_status
        RENAME TO rental_status_new
        """
    )

    # Recreate old enum
    op.execute(
        """
        CREATE TYPE rental_status AS ENUM (
            'PENDING',
            'ACTIVE',
            'RETURNED',
            'CANCELLED'
        )
        """
    )

    # Convert new values back to old values
    op.execute(
        """
        ALTER TABLE rentals
        ALTER COLUMN status TYPE rental_status
        USING (
            CASE status::text
                WHEN 'DRAFT' THEN 'PENDING'
                WHEN 'COMPLETED' THEN 'RETURNED'
                WHEN 'PARTIALLY_RETURNED' THEN 'RETURNED'
                WHEN 'OVERDUE' THEN 'ACTIVE'
                ELSE status::text
            END
        )::rental_status
        """
    )

    # Remove temporary enum
    op.execute(
        """
        DROP TYPE rental_status_new
        """
    )