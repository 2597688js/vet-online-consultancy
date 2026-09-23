"""appointment_home_visit_address

Revision ID: f2b9c5d8e1a6
Revises: e8a4b6c1d3f5
Create Date: 2026-09-23 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'f2b9c5d8e1a6'
down_revision: Union[str, Sequence[str], None] = 'e8a4b6c1d3f5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('appointments', sa.Column('home_visit_address', sa.Text(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('appointments', 'home_visit_address')
