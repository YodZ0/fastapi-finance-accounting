import datetime
import uuid

from sqlalchemy import Date, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from src.core.models import Base
from src.core.models.mixins import IntIdPkMixin
from src.core.schemas.operation import Currency


class ORMOperation(IntIdPkMixin, Base):
    name: Mapped[str] = mapped_column(nullable=False)
    amount: Mapped[float] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )
    currency: Mapped[Currency] = mapped_column(nullable=False)
    date: Mapped[datetime.date] = mapped_column(
        Date,
        nullable=False,
    )

    category_id: Mapped[int] = mapped_column(
        ForeignKey("orm_categories.id", ondelete="CASCADE"),
        nullable=False,
    )
    period_id: Mapped[int] = mapped_column(
        ForeignKey("orm_periods.id", ondelete="CASCADE"),
        nullable=False,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
