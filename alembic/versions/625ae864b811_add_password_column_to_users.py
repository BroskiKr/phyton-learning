"""add password column to users

Revision ID: 625ae864b811
Revises: 94d6fd658341
Create Date: 2024-04-28 21:01:49.536618

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from app import utils

# revision identifiers, used by Alembic.
revision: str = '625ae864b811'
down_revision: Union[str, None] = '94d6fd658341'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('password', sa.String(), nullable=True))
    op.execute(f"UPDATE users SET password = '{utils.hash('1234')}' WHERE password IS NULL")
    op.alter_column('users', 'password', nullable=False)


def downgrade() -> None:
    op.drop_column('users', 'password')
