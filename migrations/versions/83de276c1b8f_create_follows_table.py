"""Create follows table

Revision ID: 83de276c1b8f
Revises: f7bc16aee4fb
Create Date: 2023-05-29 11:52:58.610494

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '83de276c1b8f'
down_revision = 'f7bc16aee4fb'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('follows',
                    sa.Column('follower_id', sa.Integer(), nullable=False),
                    sa.Column('followee_id', sa.Integer(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.ForeignKeyConstraint(['followee_id'], ['users.id'],
                                            ondelete="CASCADE"),
                    sa.ForeignKeyConstraint(['follower_id'], ['users.id'],
                                            ondelete="CASCADE"),
                    sa.PrimaryKeyConstraint('follower_id', 'followee_id')
                    )


def downgrade() -> None:
    op.drop_table('follows')
