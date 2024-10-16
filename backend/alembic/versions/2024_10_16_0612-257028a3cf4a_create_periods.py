"""create_periods

Revision ID: 257028a3cf4a
Revises: cd92b3710e1f
Create Date: 2024-10-16 06:12:19.587988

"""

from typing import Sequence, Union

import fastapi_users_db_sqlalchemy
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "257028a3cf4a"
down_revision: Union[str, None] = "cd92b3710e1f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "orm_periods",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("start", sa.Date(), nullable=False),
        sa.Column("end", sa.Date(), nullable=False),
        sa.Column(
            "user_id",
            fastapi_users_db_sqlalchemy.generics.GUID(),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_orm_periods_user_id_users"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_orm_periods")),
    )
    op.create_index(op.f("ix_orm_periods_id"), "orm_periods", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_orm_periods_id"), table_name="orm_periods")
    op.drop_table("orm_periods")
