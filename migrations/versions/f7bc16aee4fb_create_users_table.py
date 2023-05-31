"""Create users table

Revision ID: f7bc16aee4fb
Revises: 
Create Date: 2023-05-28 17:31:11.375940

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f7bc16aee4fb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """
    id: Should we use a fixed-size id?
    settings/preferences: Consider a JSON field to store user's app-preferences there.
    photo: Add this field for storing user's photo
    """
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.Unicode(), nullable=False), # Use Unicode instead of String, in order to support non-ASCII chars
    sa.Column('first_name', sa.Unicode(), nullable=True),
    sa.Column('last_name', sa.Unicode(), nullable=True),
    sa.Column('birth', sa.DateTime(), nullable=True),
    sa.Column('email', sa.String(254), nullable=False),
    sa.Column('phone_number', sa.String(15), nullable=False),
    sa.Column('bio', sa.Unicode(160), nullable=True),
    sa.Column('is_active', sa.Boolean(), server_default='TRUE', nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('password', sa.Unicode(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('phone_number'),
    )


def downgrade() -> None:
    op.drop_table('users')
