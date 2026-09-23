"""drop_pet_color

Revision ID: a3c7e1f5d9b6
Revises: f7b1d5e9c3a2
Create Date: 2026-09-23 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'a3c7e1f5d9b6'
down_revision: Union[str, Sequence[str], None] = 'f7b1d5e9c3a2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_column('pets', 'color')


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column('pets', sa.Column('color', sa.String(), nullable=True))
