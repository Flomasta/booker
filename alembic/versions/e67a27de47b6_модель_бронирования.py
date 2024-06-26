"""модель бронирования

Revision ID: e67a27de47b6
Revises: e1582b5763b3
Create Date: 2024-05-08 09:28:31.952240

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e67a27de47b6'
down_revision: Union[str, None] = 'e1582b5763b3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('reservation',
    sa.Column('from_reserve', sa.DateTime(), nullable=True),
    sa.Column('to_reserve', sa.DateTime(), nullable=True),
    sa.Column('personal_table_id', sa.Integer(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['personal_table_id'], ['personaltable.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('reservation')
    # ### end Alembic commands ###
