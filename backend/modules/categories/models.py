from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Enum as PgEnum

from core.models import Base
from core.models.mixins import IntIdPkMixin

from .schemas import CategoryType


class ORMCategory(IntIdPkMixin, Base):
    __tablename__ = 'orm_categories'

    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    type: Mapped[CategoryType] = mapped_column(PgEnum(CategoryType), nullable=False)

    def get_related_fields(self):
        return []
