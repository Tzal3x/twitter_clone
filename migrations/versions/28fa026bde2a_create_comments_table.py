"""Create comments table

Revision ID: 28fa026bde2a
Revises: 01a547ca461e
Create Date: 2023-05-29 12:25:20.855992

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '28fa026bde2a'
down_revision = '01a547ca461e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('comments',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('body', sa.Unicode(), nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=True),
                    sa.Column('tweet_id', sa.Integer(), nullable=True),
                    sa.Column('is_active', sa.Boolean(),
                              server_default='TRUE', nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.Column('updated_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.ForeignKeyConstraint(['tweet_id'], ['tweets.id'], ),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade() -> None:
    op.drop_table('comments')
