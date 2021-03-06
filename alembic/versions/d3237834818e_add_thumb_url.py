"""add thumb_url

Revision ID: d3237834818e
Revises: 2ae539b11cfd
Create Date: 2018-08-11 15:53:13.376446

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd3237834818e'
down_revision = '2ae539b11cfd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('thumb_url', sa.String(length=100), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('posts', 'thumb_url')
    # ### end Alembic commands ###
