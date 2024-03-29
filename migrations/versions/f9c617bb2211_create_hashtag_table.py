"""Create hashtag table

Revision ID: f9c617bb2211
Revises: 937a28dc0644
Create Date: 2023-06-28 15:38:36.369267

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'f9c617bb2211'
down_revision = '937a28dc0644'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('hashtags',
    sa.Column('tweet_id', sa.Integer(), nullable=False),
    sa.Column('tags', postgresql.ARRAY(sa.Unicode(), dimensions=1), nullable=True),
    sa.ForeignKeyConstraint(['tweet_id'], ['tweets.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('tweet_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('hashtags')
    # ### end Alembic commands ###
