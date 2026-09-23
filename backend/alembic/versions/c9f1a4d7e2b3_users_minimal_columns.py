"""users_minimal_columns

Keep only what sign-in and the booking form use: id, email, password_hash, google_id, full_name, phone.

Revision ID: c9f1a4d7e2b3
Revises: b4c8e2a6d9f1
Create Date: 2026-09-23 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'c9f1a4d7e2b3'
down_revision: Union[str, Sequence[str], None] = 'b4c8e2a6d9f1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

DROPPED_COLUMNS = ('avatar_url', 'is_active', 'email_verified_at', 'deleted_at', 'created_at', 'updated_at')


def upgrade() -> None:
    """Upgrade schema."""
    for column in DROPPED_COLUMNS:
        op.drop_column('users', column)


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column('users', sa.Column('avatar_url', sa.String(), nullable=True))
    op.add_column('users', sa.Column('is_active', sa.Boolean(), server_default=sa.text('true'), nullable=False))
    op.alter_column('users', 'is_active', server_default=None)
    op.add_column('users', sa.Column('email_verified_at', sa.DateTime(), nullable=True))
    op.add_column('users', sa.Column('deleted_at', sa.DateTime(), nullable=True))
    op.add_column('users', sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False))
    op.add_column('users', sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False))
