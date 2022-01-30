"""empty message

Revision ID: 56537c6b374f
Revises: 996f01c325f1
Create Date: 2022-01-27 01:39:24.634880

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '56537c6b374f'
down_revision = '996f01c325f1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('reset_code_expire', sa.DateTime(), server_default='2022-01-27T01:39:24.561280', nullable=True))
    op.drop_column('user', 'old_token')
    op.drop_column('user', 'platform')
    op.drop_column('user', 'token')
    op.drop_column('user', 'browser')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('browser', sa.VARCHAR(), server_default=sa.text("''::character varying"), autoincrement=False, nullable=True))
    op.add_column('user', sa.Column('token', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('user', sa.Column('platform', sa.VARCHAR(), server_default=sa.text("''::character varying"), autoincrement=False, nullable=True))
    op.add_column('user', sa.Column('old_token', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('user', 'reset_code_expire')
    # ### end Alembic commands ###