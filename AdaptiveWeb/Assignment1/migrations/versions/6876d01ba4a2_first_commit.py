"""first commit

Revision ID: 6876d01ba4a2
Revises: 
Create Date: 2018-09-20 00:59:38.275257

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6876d01ba4a2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('test',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('count', sa.Integer(), nullable=True),
    sa.Column('activity', sa.String(length=64), nullable=True),
    sa.Column('time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_test_activity'), 'test', ['activity'], unique=False)
    op.create_index(op.f('ix_test_time'), 'test', ['time'], unique=False)
    op.create_index(op.f('ix_test_username'), 'test', ['username'], unique=False)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('about_me', sa.String(length=140), nullable=True),
    sa.Column('last_seen', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_test_username'), table_name='test')
    op.drop_index(op.f('ix_test_time'), table_name='test')
    op.drop_index(op.f('ix_test_activity'), table_name='test')
    op.drop_table('test')
    # ### end Alembic commands ###
