"""Create tweets table

Revision ID: 01a547ca461e
Revises: 83de276c1b8f
Create Date: 2023-05-29 12:04:04.786618

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '01a547ca461e'
down_revision = '83de276c1b8f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('tweets',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('title', sa.Unicode(), nullable=False),
                    sa.Column('body', sa.UnicodeText(), nullable=False),
                    sa.Column('is_active', sa.Boolean(),
                              server_default='TRUE', nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.Column('updated_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'],
                                            ondelete="CASCADE"),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade() -> None:
    op.drop_table('tweets')
