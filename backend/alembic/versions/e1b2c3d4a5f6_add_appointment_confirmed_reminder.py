"""add_appointment_confirmed_reminder

Revision ID: e1b2c3d4a5f6
Revises: a4d8e1c9f2b7
Create Date: 2026-08-21 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'e1b2c3d4a5f6'
down_revision: Union[str, Sequence[str], None] = 'a4d8e1c9f2b7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('appointments', sa.Column('confirmed_at', sa.DateTime(), nullable=True))
    op.add_column('appointments', sa.Column('reminder_sent_at', sa.DateTime(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('appointments', 'reminder_sent_at')
    op.drop_column('appointments', 'confirmed_at')
