"""book_consultation

Revision ID: 3c7e9a1f5b6d
Revises: 8f3c1a6b2d4e
Create Date: 2026-08-19 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '3c7e9a1f5b6d'
down_revision: Union[str, Sequence[str], None] = '8f3c1a6b2d4e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
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
        'uq_appointments_doctor_slot',
        'appointments',
        ['doctor_profile_id', 'scheduled_start'],
        unique=True,
        postgresql_where=sa.text("status != 'CANCELLED'"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index('uq_appointments_doctor_slot', table_name='appointments')

    op.drop_index(op.f('ix_pet_photos_pet_id'), table_name='pet_photos')
    op.drop_table('pet_photos')
