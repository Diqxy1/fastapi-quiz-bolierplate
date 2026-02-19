"""create_user_category_scores

Revision ID: 1c6725042ca1
Revises: 135b7f769068
Create Date: 2026-02-19 17:30:50.303449

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1c6725042ca1'
down_revision: Union[str, Sequence[str], None] = '135b7f769068'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'user_category_scores',
        sa.Column('uuid', sa.String(), primary_key=True),
        sa.Column('user_uuid', sa.String(), nullable=False),
        sa.Column('category_uuid', sa.String(), nullable=False),
        sa.Column('score', sa.Integer(), server_default='0', nullable=False),
        sa.ForeignKeyConstraint(['user_uuid'], ['users.uuid'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['category_uuid'], ['categories.uuid'], ondelete='CASCADE')
    )


def downgrade() -> None:
    op.drop_table('user_category_scores')
