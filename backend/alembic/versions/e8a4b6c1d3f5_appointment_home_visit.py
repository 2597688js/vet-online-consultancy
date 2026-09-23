"""appointment_home_visit

Revision ID: e8a4b6c1d3f5
Revises: d5e1f7a9c2b4
Create Date: 2026-09-23 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'e8a4b6c1d3f5'
down_revision: Union[str, Sequence[str], None] = 'd5e1f7a9c2b4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        'appointments',
        sa.Column('home_visit_required', sa.Boolean(), server_default=sa.text('false'), nullable=False),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('appointments', 'home_visit_required')
