"""appointments_minimal_columns

Keep only what the request form and admin dashboard use. Drops the constant consultation type /
duration / price / currency, the duplicate owner_id (the pet links to its owner), the unused
updated_at, the time-slot and reminder columns, and the status-change timestamps.

Revision ID: e5a9c3f7b2d4
Revises: d2e6b8f3a1c7
Create Date: 2026-09-23 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'e5a9c3f7b2d4'
down_revision: Union[str, Sequence[str], None] = 'd2e6b8f3a1c7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

DROPPED_COLUMNS = (
    'consultation_type', 'duration_minutes', 'price_at_booking', 'currency',
    'scheduled_start', 'scheduled_end', 'reminder_sent_at',
    'confirmed_at', 'completed_at', 'cancelled_at', 'updated_at',
)


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_index('ix_appointments_owner_status', table_name='appointments')
    op.drop_index('ix_appointments_scheduled_start', table_name='appointments')
    op.drop_constraint('appointments_owner_id_fkey', 'appointments', type_='foreignkey')
    op.drop_column('appointments', 'owner_id')
    for column in DROPPED_COLUMNS:
        op.drop_column('appointments', column)
    postgresql.ENUM(name='consultation_type').drop(op.get_bind())


def downgrade() -> None:
    """Downgrade schema."""
    consultation_type = postgresql.ENUM('VIDEO', 'AUDIO', 'CHAT', name='consultation_type')
    consultation_type.create(op.get_bind())
    op.add_column('appointments', sa.Column('consultation_type', consultation_type, server_default='VIDEO', nullable=False))
    op.add_column('appointments', sa.Column('duration_minutes', sa.Integer(), server_default='30', nullable=False))
    op.add_column('appointments', sa.Column('price_at_booking', sa.Numeric(precision=10, scale=2), server_default='0', nullable=False))
    op.add_column('appointments', sa.Column('currency', sa.String(), server_default='INR', nullable=False))
    for column in ('consultation_type', 'duration_minutes', 'price_at_booking', 'currency'):
        op.alter_column('appointments', column, server_default=None)
    for column in ('scheduled_start', 'scheduled_end', 'reminder_sent_at', 'confirmed_at', 'completed_at', 'cancelled_at'):
        op.add_column('appointments', sa.Column(column, sa.DateTime(), nullable=True))
    op.add_column('appointments', sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False))

    op.add_column('appointments', sa.Column('owner_id', sa.UUID(), nullable=True))
    op.execute("UPDATE appointments a SET owner_id = p.owner_id FROM pets p WHERE p.id = a.pet_id")
    op.alter_column('appointments', 'owner_id', nullable=False)
    op.create_foreign_key('appointments_owner_id_fkey', 'appointments', 'users', ['owner_id'], ['id'], ondelete='RESTRICT')
    op.create_index('ix_appointments_owner_status', 'appointments', ['owner_id', 'status'], unique=False)
    op.create_index('ix_appointments_scheduled_start', 'appointments', ['scheduled_start'], unique=False)
