"""create posts table

Revision ID: 6787224dcc99
Revises: 
Create Date: 2024-04-15 21:31:24.254994

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6787224dcc99'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table('posts',
                    sa.Column('id',sa.Integer(),nullable=False,primary_key=True),
                    sa.Column('title',sa.String(),nullable=False),
                    sa.Column('body',sa.String(),nullable=False)
                    )



def downgrade():
    op.drop_table('posts')
