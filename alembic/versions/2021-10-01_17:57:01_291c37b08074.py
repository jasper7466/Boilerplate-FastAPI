"""Add table 'refresh_tokens'

Revision ID: 291c37b08074
Revises: 6073f90c5a44
Create Date: 2021-10-01 17:57:01.165680

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '291c37b08074'
down_revision = '6073f90c5a44'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'refresh_tokens',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('account_id', sa.Integer(), nullable=False),
        sa.Column('token', sa.String(), nullable=False),
        sa.ForeignKeyConstraint(['account_id'], ['accounts.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('account_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('refresh_tokens')
    # ### end Alembic commands ###
