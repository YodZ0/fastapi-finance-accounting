from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.sqltypes import JSON, String

from core.models import Base
from core.models.mixins import IntIdPkMixin


class ORMRole(IntIdPkMixin, Base):
    name: Mapped[str] = mapped_column(String(length=320), unique=True, nullable=False)
    permissions: Mapped[JSON] = mapped_column(JSON, nullable=False)
