"""add users

Revision ID: 14baae79cdc6
Revises: 432bffabb2a5
Create Date: 2024-04-18 17:00:30.884502

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from app import models

# revision identifiers, used by Alembic.
revision: str = '14baae79cdc6'
down_revision: Union[str, None] = '432bffabb2a5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.bulk_insert(models.User.__table__,[{
        "first_name":"admin",
        "last_name":"admin",
    },
    {
        "first_name":"Andrij",
        "last_name":"Krokhmalnyy",
    },
    {
        "first_name":"Vasyl",
        "last_name":"Khomiv",
    },
    {
        "first_name":"Elon",
        "last_name":"Musk",
    },
    {
        "first_name":"Cristiano",
        "last_name":"Ronaldo",
    }
    ])


def downgrade() -> None:
    op.execute("""DELETE FROM users
        WHERE (first_name = 'admin' AND last_name = 'admin')
        OR (first_name = 'Andrij' AND last_name = 'Krokhmalnyy')
        OR (first_name = 'Vasyl' AND last_name = 'Khomiv')
        OR (first_name = 'Elon' AND last_name = 'Musk')
        OR (first_name = 'Cristiano' AND last_name = 'Ronaldo');""")
