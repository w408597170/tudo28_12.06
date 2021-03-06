"""add img_url table

Revision ID: 2b6a6b023427
Revises: 948d3e7e8407
Create Date: 2018-11-25 00:13:51.019019

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2b6a6b023427'
down_revision = '948d3e7e8407'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('img_url',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('image_url', sa.String(length=100), nullable=True),
    sa.Column('thumb_url', sa.String(length=100), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('img_url')
    # ### end Alembic commands ###
