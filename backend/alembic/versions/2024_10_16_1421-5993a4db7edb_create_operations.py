"""create_operations

Revision ID: 5993a4db7edb
Revises: 257028a3cf4a
Create Date: 2024-10-16 14:21:29.991281

"""

from typing import Sequence, Union

import fastapi_users_db_sqlalchemy
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "5993a4db7edb"
down_revision: Union[str, None] = "257028a3cf4a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "orm_operations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("amount", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column(
            "currency",
            sa.Enum("KZT", "RUB", "USD", "EUR", "KRW", name="currency"),
            nullable=False,
        ),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("category_id", sa.Integer(), nullable=False),
        sa.Column("period_id", sa.Integer(), nullable=False),
        sa.Column(
            "user_id",
            fastapi_users_db_sqlalchemy.generics.GUID(),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["category_id"],
            ["orm_categories.id"],
            name=op.f("fk_orm_operations_category_id_orm_categories"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["period_id"],
            ["orm_periods.id"],
            name=op.f("fk_orm_operations_period_id_orm_periods"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_orm_operations_user_id_users"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_orm_operations")),
    )
    op.create_index(
        op.f("ix_orm_operations_id"), "orm_operations", ["id"], unique=False
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_orm_operations_id"), table_name="orm_operations")
    op.drop_table("orm_operations")
