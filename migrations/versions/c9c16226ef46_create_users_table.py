"""create_users_table

Revision ID: c9c16226ef46
Revises: 
Create Date: 2026-02-19 12:05:05.075091

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c9c16226ef46'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('uuid', sa.String(), primary_key=True),
        sa.Column('username', sa.String(), nullable=False, unique=True),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('is_staff', sa.Boolean(), nullable=True),
        sa.Column('total_score', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now(), nullable=True),
    )


def downgrade() -> None:
    op.drop_table('users')
