"""Add due_date and priority fields to tasks table

Revision ID: dcfb57b0c4d1
Revises:
Create Date: 2026-01-20 21:24:04.956786

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dcfb57b0c4d1'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add the new columns to the tasks table
    op.add_column('tasks', sa.Column('due_date', sa.DateTime(), nullable=True))
    op.add_column('tasks', sa.Column('priority', sa.String(length=20), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    # Remove the columns we added
    op.drop_column('tasks', 'priority')
    op.drop_column('tasks', 'due_date')
