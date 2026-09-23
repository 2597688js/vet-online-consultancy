"""pets_minimal_columns

Drop pets columns the app no longer uses: existing_conditions (replaced by medical_history),
deleted_at (never set), created_at and updated_at (never shown).

Revision ID: d2e6b8f3a1c7
Revises: c9f1a4d7e2b3
Create Date: 2026-09-23 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'd2e6b8f3a1c7'
down_revision: Union[str, Sequence[str], None] = 'c9f1a4d7e2b3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

DROPPED_COLUMNS = ('existing_conditions', 'deleted_at', 'created_at', 'updated_at')


def upgrade() -> None:
    """Upgrade schema."""
    for column in DROPPED_COLUMNS:
        op.drop_column('pets', column)


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column('pets', sa.Column('existing_conditions', sa.Text(), nullable=True))
    op.add_column('pets', sa.Column('deleted_at', sa.DateTime(), nullable=True))
    op.add_column('pets', sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False))
    op.add_column('pets', sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False))
