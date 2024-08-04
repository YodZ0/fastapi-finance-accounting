"""initial

Revision ID: 927cb3debee1
Revises: 
Create Date: 2024-08-05 01:36:14.998106

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "927cb3debee1"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "orm_operations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("amount", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column("currency", sa.String(), nullable=False),
        sa.Column("kind", sa.String(), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_orm_operations")),
    )


def downgrade() -> None:
    op.drop_table("orm_operations")
