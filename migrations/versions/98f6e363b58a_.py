"""empty message

Revision ID: 98f6e363b58a
Revises: 7a5f6fc36dd6
Create Date: 2022-03-13 20:14:01.077528

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '98f6e363b58a'
down_revision = '7a5f6fc36dd6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('permission',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('alias', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('permission')
    # ### end Alembic commands ###