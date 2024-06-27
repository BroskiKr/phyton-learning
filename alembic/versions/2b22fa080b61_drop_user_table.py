"""Drop user table

Revision ID: 2b22fa080b61
Revises: 7894418f9e57
Create Date: 2024-06-12 17:20:28.411137

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from app import models


# revision identifiers, used by Alembic.
revision: str = "2b22fa080b61"
down_revision: Union[str, None] = "7894418f9e57"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint("post_users_fk", table_name="posts")
    op.drop_table("users")


def downgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("first_name", sa.String(), nullable=False),
        sa.Column("last_name", sa.String(), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )

    op.bulk_insert(
        models.User.__table__,
        [
            {
                "first_name": "admin",
                "last_name": "admin",
            },
            {
                "first_name": "Andrij",
                "last_name": "Krokhmalnyy",
            },
            {
                "first_name": "Vasyl",
                "last_name": "Khomiv",
            },
            {
                "first_name": "Elon",
                "last_name": "Musk",
            },
            {
                "first_name": "Cristiano",
                "last_name": "Ronaldo",
            },
        ],
    )

    op.add_column("users", sa.Column("password", sa.String(), nullable=True))
    op.execute(
        f"UPDATE users SET password = '$2b$12$c/hk9viBU9LLX1I2FRcYGuijgxv6Js0gf3vV0rLfsiNkwJ/CmGeR.' WHERE password IS NULL"
    )
    op.alter_column("users", "password", nullable=False)

    op.add_column("users", sa.Column("email", sa.String(), nullable=True))
    op.execute(
        f"UPDATE users SET email = 'krohmalnyj.andr@gmail.com' WHERE last_name='Krokhmalnyy'"
    )
    op.execute(f"UPDATE users SET email = 'somegmail@gmail.com' WHERE email IS NULL ")
    op.alter_column("users", "email", nullable=False)

    op.create_foreign_key(
        "post_users_fk",
        source_table="posts",
        referent_table="users",
        local_cols=["owner_id"],
        remote_cols=["id"],
        ondelete="CASCADE",
    )
