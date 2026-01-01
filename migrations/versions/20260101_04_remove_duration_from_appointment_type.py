"""
Remove duration column from appointment_types
Revision ID: 20260101_04_remove_duration_from_appointment_type
Revises: f16e951f9ae1_add_payment_method_to_invoice
Create Date: 2026-01-01 18:16:33.980000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20260101_04_remove_duration_from_appointment_type'
down_revision = 'f16e951f9ae1'
branch_labels = None
depends_on = None

def upgrade():
    op.drop_column('appointment_types', 'duration')

def downgrade():
    op.add_column('appointment_types', sa.Column('duration', sa.Integer))
