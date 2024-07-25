from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Numeric, Date

from core.models import Base


class ORMOperation(Base):
    title: Mapped[str]
    amount: Mapped[float] = mapped_column(Numeric(10, 2))
    currency: Mapped[str]
    kind: Mapped[str]
    date: Mapped[str] = mapped_column(Date)
