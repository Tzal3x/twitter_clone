"""Create basic database

Revision ID: 937a28dc0644
Revises:
Create Date: 2023-06-13 19:41:22.825012

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils

# revision identifiers, used by Alembic.
revision = '937a28dc0644'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('username', sa.Unicode(length=20),
                              nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('first_name', sa.Unicode(length=40),
                              nullable=True),
                    sa.Column('last_name', sa.Unicode(length=40),
                              nullable=True),
                    sa.Column('birth', sa.DateTime(), nullable=False),
                    sa.Column('email', sqlalchemy_utils.types.email.EmailType(
                        length=255), nullable=False),
                    sa.Column('phone_number', sa.String(length=15)),
                    sa.Column('bio', sa.Unicode(length=250), nullable=True),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('NOW()'), nullable=False),
                    sa.Column('updated_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('NOW()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email'),
                    sa.UniqueConstraint('phone_number'),
                    sa.UniqueConstraint('username')
                    )
    op.create_table('follows',
                    sa.Column('follower_id', sa.Integer(), nullable=False),
                    sa.Column('followee_id', sa.Integer(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('NOW()'), nullable=False),
                    sa.ForeignKeyConstraint(['followee_id'], ['users.id'],
                                            ondelete='CASCADE'),
                    sa.ForeignKeyConstraint(['follower_id'], ['users.id'],
                                            ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('follower_id', 'followee_id')
                    )
    op.create_table('tweets',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('title', sa.Unicode(length=250),
                              nullable=False),
                    sa.Column('body', sa.Unicode(length=10000),
                              nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('NOW()'), nullable=False),
                    sa.Column('updated_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('NOW()'), nullable=False),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'],
                                            ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('comments',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('body', sa.Unicode(length=500), nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('tweet_id', sa.Integer(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('NOW()'), nullable=False),
                    sa.Column('updated_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('NOW()'), nullable=False),
                    sa.ForeignKeyConstraint(['tweet_id'], ['tweets.id'],
                                            ondelete='CASCADE'),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'],
                                            ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('tweet_likes',
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('tweet_id', sa.Integer(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('NOW()'), nullable=False),
                    sa.Column('updated_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('NOW()'), nullable=False),
                    sa.ForeignKeyConstraint(['tweet_id'], ['tweets.id'],
                                            ondelete='CASCADE'),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'],
                                            ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('user_id', 'tweet_id')
                    )
    op.create_table('comment_likes',
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('comment_id', sa.Integer(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('NOW()'), nullable=False),
                    sa.Column('updated_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('NOW()'), nullable=False),
                    sa.ForeignKeyConstraint(['comment_id'], ['comments.id'],
                                            ondelete='CASCADE'),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'],
                                            ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('user_id', 'comment_id')
                    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('comment_likes')
    op.drop_table('tweet_likes')
    op.drop_table('comments')
    op.drop_table('tweets')
    op.drop_table('follows')
    op.drop_table('users')
    # ### end Alembic commands ###