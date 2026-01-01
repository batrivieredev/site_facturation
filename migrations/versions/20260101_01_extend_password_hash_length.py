"""
extend password_hash length in users table
Revision ID: 20260101_01
Revises: d432150aff4d
Create Date: 2026-01-01 14:31:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20260101_01'
down_revision = 'd432150aff4d'
branch_labels = None
depends_on = None

def upgrade():
    op.alter_column('users', 'password_hash',
        existing_type=sa.String(length=128),
        type_=sa.String(length=512),
        existing_nullable=False)

def downgrade():
    op.alter_column('users', 'password_hash',
        existing_type=sa.String(length=512),
        type_=sa.String(length=128),
        existing_nullable=False)
