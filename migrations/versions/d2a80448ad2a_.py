"""empty message

Revision ID: d2a80448ad2a
Revises: 
Create Date: 2021-04-17 21:20:47.857130

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd2a80448ad2a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('center',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('position', sa.Integer(), nullable=False),
    sa.Column('weight', sa.Float(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('symbol', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('products',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('email', sa.String(length=128), nullable=True),
    sa.Column('password_hash', sa.String(length=256), nullable=True),
    sa.Column('token', sa.String(), nullable=True),
    sa.Column('old_token', sa.String(), nullable=True),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('role', sa.String(length=12), server_default='user', nullable=True),
    sa.Column('platform', sa.String(), server_default='', nullable=True),
    sa.Column('browser', sa.String(), server_default='', nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    op.drop_table('products')
    op.drop_table('center')
    # ### end Alembic commands ###
