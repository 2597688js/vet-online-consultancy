"""users_phone_nullable

Revision ID: 8f3c1a6b2d4e
Revises: 06d2eaa12721
Create Date: 2026-08-13 12:10:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '8f3c1a6b2d4e'
down_revision: Union[str, Sequence[str], None] = '06d2eaa12721'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column('users', 'phone', existing_type=sa.String(), nullable=True)


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column('users', 'phone', existing_type=sa.String(), nullable=False)
