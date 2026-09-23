"""drop_cancellation_reason

Revision ID: f7b1d5e9c3a2
Revises: e5a9c3f7b2d4
Create Date: 2026-09-23 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'f7b1d5e9c3a2'
down_revision: Union[str, Sequence[str], None] = 'e5a9c3f7b2d4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_column('appointments', 'cancellation_reason')


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column('appointments', sa.Column('cancellation_reason', sa.Text(), nullable=True))
