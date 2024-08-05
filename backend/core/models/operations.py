from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Numeric, Date

from core.models import Base
from core.models.mixins import IntIdPkMixin
from core.schemas import OperationBase


class ORMOperation(IntIdPkMixin, Base):
    title: Mapped[str]
    amount: Mapped[float] = mapped_column(Numeric(10, 2))
    currency: Mapped[str]
    kind: Mapped[str]
    category: Mapped[str]
    date: Mapped[datetime.date] = mapped_column(Date)

    def to_read_model(self) -> OperationBase:
        return OperationBase(
            id=self.id,
            title=self.title,
            amount=self.amount,
            currency=self.currency,
            kind=self.kind,
            category=self.category,
            date=self.date,
        )
