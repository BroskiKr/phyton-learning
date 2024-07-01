"""create email column

Revision ID: 7894418f9e57
Revises: 625ae864b811
Create Date: 2024-05-29 18:29:47.799716

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "7894418f9e57"
down_revision: Union[str, None] = "625ae864b811"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("email", sa.String(), nullable=True))
    op.execute(
        f"UPDATE users SET email = 'krohmalnyj.andr@gmail.com' WHERE last_name='Krokhmalnyy'"
    )
    op.execute(f"UPDATE users SET email = 'somegmail@gmail.com' WHERE email IS NULL ")
    op.alter_column("users", "email", nullable=False)


def downgrade() -> None:
    op.drop_column("users", "email")
