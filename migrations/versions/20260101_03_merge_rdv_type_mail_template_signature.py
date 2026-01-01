"""
Merge migration: rdv_type client + mail template/signature
Revision ID: 20260101_03_merge_rdv_type_mail_template_signature
Revises: 20260101_01
Create Date: 2026-01-01 15:40:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20260101_03_merge_rdv_type_mail_template_signature'
down_revision = '20260101_01'
branch_labels = None
depends_on = None

def upgrade():
    # Ajout du champ rdv_type dans clients
    with op.batch_alter_table('clients', schema=None) as batch_op:
        batch_op.add_column(sa.Column('rdv_type', sa.String(length=100), nullable=True))
    # Création des tables mail_templates et mail_signatures
    op.create_table(
        'mail_templates',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('body', sa.Text, nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=False)
    )
    op.create_table(
        'mail_signatures',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('signature', sa.Text, nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=False)
    )

def downgrade():
    # Suppression du champ rdv_type dans clients
    with op.batch_alter_table('clients', schema=None) as batch_op:
        batch_op.drop_column('rdv_type')
    # Suppression des tables mail_templates et mail_signatures
    op.drop_table('mail_templates')
    op.drop_table('mail_signatures')
