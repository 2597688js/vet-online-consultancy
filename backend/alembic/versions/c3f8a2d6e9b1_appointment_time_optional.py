"""appointment_time_optional

Revision ID: c3f8a2d6e9b1
Revises: b7c2d9e4f1a3
Create Date: 2026-09-23 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'c3f8a2d6e9b1'
down_revision: Union[str, Sequence[str], None] = 'b7c2d9e4f1a3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column('appointments', 'scheduled_start', existing_type=sa.DateTime(), nullable=True)
    op.alter_column('appointments', 'scheduled_end', existing_type=sa.DateTime(), nullable=True)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("UPDATE appointments SET scheduled_start = created_at WHERE scheduled_start IS NULL")
    op.execute("UPDATE appointments SET scheduled_end = scheduled_start + interval '30 minutes' WHERE scheduled_end IS NULL")
    op.alter_column('appointments', 'scheduled_end', existing_type=sa.DateTime(), nullable=False)
    op.alter_column('appointments', 'scheduled_start', existing_type=sa.DateTime(), nullable=False)
