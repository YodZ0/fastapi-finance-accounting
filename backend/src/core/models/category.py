from sqlalchemy.orm import Mapped, mapped_column

from src.core.models import Base
from src.core.models.mixins import IntIdPkMixin

from src.core.schemas.category import CategoryType


class ORMCategory(IntIdPkMixin, Base):
    __tablename__ = "orm_categories"

    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    type: Mapped[CategoryType] = mapped_column(nullable=False)
