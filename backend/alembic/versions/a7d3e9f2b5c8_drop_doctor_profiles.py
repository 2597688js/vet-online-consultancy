"""drop_doctor_profiles

Single-doctor practice: requests no longer link to a doctor profile. Dr. Sarkar is the ADMIN user.

Revision ID: a7d3e9f2b5c8
Revises: f2b9c5d8e1a6
Create Date: 2026-09-23 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'a7d3e9f2b5c8'
down_revision: Union[str, Sequence[str], None] = 'f2b9c5d8e1a6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_index('ix_appointments_doctor_scheduled_start', table_name='appointments')
    op.drop_constraint('appointments_doctor_profile_id_fkey', 'appointments', type_='foreignkey')
    op.drop_column('appointments', 'doctor_profile_id')
    op.drop_index(op.f('ix_doctor_profiles_verification_status'), table_name='doctor_profiles')
    op.drop_index(op.f('ix_doctor_profiles_specialty'), table_name='doctor_profiles')
    op.drop_table('doctor_profiles')
    postgresql.ENUM(name='verification_status').drop(op.get_bind())


def downgrade() -> None:
    """Downgrade schema."""
    op.create_table('doctor_profiles',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('specialty', sa.String(), nullable=False),
    sa.Column('specializations', postgresql.ARRAY(sa.String()), nullable=False),
    sa.Column('license_number', sa.String(), nullable=True),
    sa.Column('years_of_experience', sa.Integer(), nullable=False),
    sa.Column('education', sa.Text(), nullable=True),
    sa.Column('languages', postgresql.ARRAY(sa.String()), nullable=False),
    sa.Column('bio', sa.Text(), nullable=True),
    sa.Column('rating', sa.Numeric(precision=3, scale=2), nullable=False),
    sa.Column('rating_count', sa.Integer(), nullable=False),
    sa.Column('verification_status', postgresql.ENUM('PENDING', 'VERIFIED', 'REJECTED', 'SUSPENDED', name='verification_status'), nullable=False),
    sa.Column('verified_at', sa.DateTime(), nullable=True),
    sa.Column('verified_by_id', sa.UUID(), nullable=True),
    sa.Column('is_accepting_appointments', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['verified_by_id'], ['users.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('license_number'),
    sa.UniqueConstraint('user_id')
    )
    op.create_index(op.f('ix_doctor_profiles_specialty'), 'doctor_profiles', ['specialty'], unique=False)
    op.create_index(op.f('ix_doctor_profiles_verification_status'), 'doctor_profiles', ['verification_status'], unique=False)
    # Recreate the doctor's profile from her ADMIN account and link every request to it.
    op.execute("""
        INSERT INTO doctor_profiles (id, user_id, specialty, specializations, years_of_experience, languages,
                                     rating, rating_count, verification_status, is_accepting_appointments)
        SELECT gen_random_uuid(), id, 'General Veterinary Medicine', '{}', 0, '{}', 0, 0, 'VERIFIED', true
        FROM users WHERE role = 'ADMIN' ORDER BY created_at LIMIT 1
    """)
    op.add_column('appointments', sa.Column('doctor_profile_id', sa.UUID(), nullable=True))
    op.execute("UPDATE appointments SET doctor_profile_id = (SELECT id FROM doctor_profiles LIMIT 1)")
    op.alter_column('appointments', 'doctor_profile_id', nullable=False)
    op.create_foreign_key(
        'appointments_doctor_profile_id_fkey', 'appointments', 'doctor_profiles',
        ['doctor_profile_id'], ['id'], ondelete='RESTRICT',
    )
    op.create_index('ix_appointments_doctor_scheduled_start', 'appointments', ['doctor_profile_id', 'scheduled_start'], unique=False)
