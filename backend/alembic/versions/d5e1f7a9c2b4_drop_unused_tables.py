"""drop_unused_tables

Pet photos, payments and consultation offerings are no longer part of the app, and bookings
no longer have slots, so the per-slot unique index goes too.

Revision ID: d5e1f7a9c2b4
Revises: c3f8a2d6e9b1
Create Date: 2026-09-23 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'd5e1f7a9c2b4'
down_revision: Union[str, Sequence[str], None] = 'c3f8a2d6e9b1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_index('uq_appointments_doctor_slot', table_name='appointments')

    op.drop_index(op.f('ix_pet_photos_pet_id'), table_name='pet_photos')
    op.drop_table('pet_photos')
    op.drop_column('pets', 'photo_url')

    op.drop_index(op.f('ix_payments_status'), table_name='payments')
    op.drop_index(op.f('ix_payments_payer_id'), table_name='payments')
    op.drop_index(op.f('ix_payments_created_at'), table_name='payments')
    op.drop_index(op.f('ix_payments_appointment_id'), table_name='payments')
    op.drop_table('payments')
    postgresql.ENUM(name='payment_status').drop(op.get_bind())

    op.drop_constraint('appointments_consultation_offering_id_fkey', 'appointments', type_='foreignkey')
    op.drop_column('appointments', 'consultation_offering_id')
    op.drop_index(op.f('ix_consultation_offerings_type'), table_name='consultation_offerings')
    op.drop_index(op.f('ix_consultation_offerings_doctor_profile_id'), table_name='consultation_offerings')
    op.drop_table('consultation_offerings')


def downgrade() -> None:
    """Downgrade schema."""
    op.create_table('consultation_offerings',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('doctor_profile_id', sa.UUID(), nullable=False),
    sa.Column('type', postgresql.ENUM('VIDEO', 'AUDIO', 'CHAT', name='consultation_type', create_type=False), nullable=False),
    sa.Column('duration_minutes', sa.Integer(), nullable=False),
    sa.Column('price', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('currency', sa.String(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['doctor_profile_id'], ['doctor_profiles.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('doctor_profile_id', 'type')
    )
    op.create_index(op.f('ix_consultation_offerings_doctor_profile_id'), 'consultation_offerings', ['doctor_profile_id'], unique=False)
    op.create_index(op.f('ix_consultation_offerings_type'), 'consultation_offerings', ['type'], unique=False)
    op.add_column('appointments', sa.Column('consultation_offering_id', sa.UUID(), nullable=True))
    op.create_foreign_key(
        'appointments_consultation_offering_id_fkey', 'appointments', 'consultation_offerings',
        ['consultation_offering_id'], ['id'], ondelete='SET NULL',
    )

    op.create_table('payments',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('appointment_id', sa.UUID(), nullable=False),
    sa.Column('payer_id', sa.UUID(), nullable=False),
    sa.Column('transaction_id', sa.String(), nullable=True),
    sa.Column('amount', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('platform_fee', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('total_amount', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('currency', sa.String(), nullable=False),
    sa.Column('status', postgresql.ENUM('PENDING', 'PAID', 'FAILED', 'REFUNDED', name='payment_status'), nullable=False),
    sa.Column('method', sa.String(), nullable=True),
    sa.Column('provider', sa.String(), nullable=True),
    sa.Column('paid_at', sa.DateTime(), nullable=True),
    sa.Column('failed_at', sa.DateTime(), nullable=True),
    sa.Column('failure_reason', sa.Text(), nullable=True),
    sa.Column('refunded_at', sa.DateTime(), nullable=True),
    sa.Column('refund_amount', sa.Numeric(precision=10, scale=2), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['appointment_id'], ['appointments.id'], ondelete='RESTRICT'),
    sa.ForeignKeyConstraint(['payer_id'], ['users.id'], ondelete='RESTRICT'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('transaction_id')
    )
    op.create_index(op.f('ix_payments_appointment_id'), 'payments', ['appointment_id'], unique=False)
    op.create_index(op.f('ix_payments_created_at'), 'payments', ['created_at'], unique=False)
    op.create_index(op.f('ix_payments_payer_id'), 'payments', ['payer_id'], unique=False)
    op.create_index(op.f('ix_payments_status'), 'payments', ['status'], unique=False)

    op.add_column('pets', sa.Column('photo_url', sa.String(), nullable=True))
    op.create_table(
        'pet_photos',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('pet_id', sa.UUID(), nullable=False),
        sa.Column('url', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['pet_id'], ['pets.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_pet_photos_pet_id'), 'pet_photos', ['pet_id'], unique=False)

    op.create_index(
        'uq_appointments_doctor_slot', 'appointments', ['doctor_profile_id', 'scheduled_start'],
        unique=True, postgresql_where=sa.text("status != 'CANCELLED'"),
    )
