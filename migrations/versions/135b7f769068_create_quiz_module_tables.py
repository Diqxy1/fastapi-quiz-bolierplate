"""create_quiz_module_tables

Revision ID: 135b7f769068
Revises: b54097bf451a
Create Date: 2026-02-19 15:11:54.697525

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '135b7f769068'
down_revision: Union[str, Sequence[str], None] = 'b54097bf451a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'categories',
        sa.Column('uuid', sa.String(), primary_key=True),
        sa.Column('name', sa.String(length=100), nullable=False, unique=True),
        sa.Column('description', sa.String(length=255), nullable=True)
    )

    op.create_table(
        'questions',
        sa.Column('uuid', sa.String(), primary_key=True),
        sa.Column('text', sa.String(), nullable=False),
        sa.Column('category_uuid', sa.String(), nullable=False),
        sa.ForeignKeyConstraint(['category_uuid'], ['categories.uuid'], ondelete='CASCADE')
    )

    op.create_table(
        'choices',
        sa.Column('uuid', sa.String(), primary_key=True),
        sa.Column('text', sa.String(), nullable=False),
        sa.Column('is_correct', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('question_uuid', sa.String(), nullable=False),
        sa.ForeignKeyConstraint(['question_uuid'], ['questions.uuid'], ondelete='CASCADE'),
    )


def downgrade() -> None:
    op.drop_table('choices')
    op.drop_table('questions')
    op.drop_table('categories')
