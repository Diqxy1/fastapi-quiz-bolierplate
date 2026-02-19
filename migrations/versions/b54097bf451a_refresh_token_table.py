"""refresh_token_table

Revision ID: b54097bf451a
Revises: c9c16226ef46
Create Date: 2026-02-19 13:08:58.288999

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b54097bf451a'
down_revision: Union[str, Sequence[str], None] = 'c9c16226ef46'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'refresh_tokens',
        sa.Column('uuid', sa.String(), nullable=False, primary_key=True),
        sa.Column('token', sa.String(), nullable=False, unique=True, index=True),
        sa.Column('user_uuid', sa.String(), sa.ForeignKey('users.uuid', ondelete='CASCADE'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('revoked', sa.Boolean(), nullable=False, default=False),
    )


def downgrade() -> None:
    op.drop_table("refresh_tokens")
