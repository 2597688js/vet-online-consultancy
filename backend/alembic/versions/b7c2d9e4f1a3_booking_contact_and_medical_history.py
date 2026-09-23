"""booking_contact_and_medical_history

Revision ID: b7c2d9e4f1a3
Revises: e1b2c3d4a5f6
Create Date: 2026-09-23 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'b7c2d9e4f1a3'
down_revision: Union[str, Sequence[str], None] = 'e1b2c3d4a5f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('appointments', sa.Column('contact_name', sa.String(), nullable=True))
    op.add_column('appointments', sa.Column('contact_phone', sa.String(), nullable=True))
    op.add_column('pets', sa.Column('medical_history', sa.Text(), nullable=True))
    op.alter_column('pets', 'name', existing_type=sa.String(), nullable=True)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("UPDATE pets SET name = species WHERE name IS NULL")
    op.alter_column('pets', 'name', existing_type=sa.String(), nullable=False)
    op.drop_column('pets', 'medical_history')
    op.drop_column('appointments', 'contact_phone')
    op.drop_column('appointments', 'contact_name')
