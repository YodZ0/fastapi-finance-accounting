import datetime
import uuid

from sqlalchemy import Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.core.models import Base
from src.core.models.mixins import IntIdPkMixin


class ORMPeriod(IntIdPkMixin, Base):
    name: Mapped[str] = mapped_column(nullable=False)
    start: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    end: Mapped[datetime.date] = mapped_column(Date, nullable=False)

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
