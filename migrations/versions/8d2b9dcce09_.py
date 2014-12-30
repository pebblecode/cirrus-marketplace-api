"""empty message

Revision ID: 8d2b9dcce09
Revises: None
Create Date: 2014-12-29 17:11:52.985783

"""

# revision identifiers, used by Alembic.
revision = '8d2b9dcce09'
down_revision = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('services',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('data', postgresql.JSON(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('services')
    ### end Alembic commands ###
