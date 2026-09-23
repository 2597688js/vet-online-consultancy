"""drop_doctor_availabilities

Revision ID: a4d8e1c9f2b7
Revises: 3c7e9a1f5b6d
Create Date: 2026-08-20 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'a4d8e1c9f2b7'
down_revision: Union[str, Sequence[str], None] = '3c7e9a1f5b6d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_index('ix_doctor_availabilities_profile_day', table_name='doctor_availabilities')
    op.drop_index(op.f('ix_doctor_availabilities_doctor_profile_id'), table_name='doctor_availabilities')
    op.drop_index(op.f('ix_doctor_availabilities_day_of_week'), table_name='doctor_availabilities')
    op.drop_table('doctor_availabilities')


def downgrade() -> None:
    """Downgrade schema."""
    op.create_table(
        'doctor_availabilities',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('doctor_profile_id', sa.UUID(), nullable=False),
        sa.Column('day_of_week', sa.SmallInteger(), nullable=False),
        sa.Column('start_time', sa.SmallInteger(), nullable=False),
        sa.Column('end_time', sa.SmallInteger(), nullable=False),
        sa.Column('buffer_minutes', sa.Integer(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['doctor_profile_id'], ['doctor_profiles.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('doctor_profile_id', 'day_of_week', 'start_time', 'end_time'),
    )
    op.create_index(op.f('ix_doctor_availabilities_day_of_week'), 'doctor_availabilities', ['day_of_week'], unique=False)
    op.create_index(op.f('ix_doctor_availabilities_doctor_profile_id'), 'doctor_availabilities', ['doctor_profile_id'], unique=False)
    op.create_index('ix_doctor_availabilities_profile_day', 'doctor_availabilities', ['doctor_profile_id', 'day_of_week'], unique=False)
