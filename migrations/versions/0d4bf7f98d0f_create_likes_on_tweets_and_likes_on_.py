"""Create likes_on_tweets and likes_on_comments tables

Revision ID: 0d4bf7f98d0f
Revises: 28fa026bde2a
Create Date: 2023-05-29 12:33:51.680403

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0d4bf7f98d0f'
down_revision = '28fa026bde2a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('tweet_likes',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('tweet_id', sa.Integer(), nullable=False),
    sa.Column('is_active', sa.Boolean(), server_default=True, nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['tweet_id'], ['tweets.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'tweet_id')
    )
    op.create_table('comment_likes',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('comment_id', sa.Integer(), nullable=False),
    sa.Column('is_active', sa.Boolean(), server_default=True, nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['comment_id'], ['comments.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'comment_id')
    )


def downgrade() -> None:
    op.drop_table('comment_likes')
    op.drop_table('tweet_likes')
