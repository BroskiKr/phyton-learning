"""Change type of owner_id column

Revision ID: 41108a12eaa4
Revises: 2b22fa080b61
Create Date: 2024-06-17 14:22:27.252532

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "41108a12eaa4"
down_revision: Union[str, None] = "2b22fa080b61"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "posts",
        "owner_id",
        type_=sa.String(),
        postgresql_using="owner_id::character varying",
    )


def downgrade() -> None:
    op.alter_column(
        "posts", "owner_id", type_=sa.Integer(), postgresql_using="owner_id::integer"
    )
