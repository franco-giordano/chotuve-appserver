"""empty message

Revision ID: 2fc0025249b2
Revises: 23dd7083d200
Create Date: 2020-07-02 02:46:24.204194

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2fc0025249b2'
down_revision = '23dd7083d200'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('videos', sa.Column('view_count', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('videos', 'view_count')
    # ### end Alembic commands ###
