from core.models import ORMOperation
from .repository import SQLAlchemyRepository


class OperationsRepository(SQLAlchemyRepository):
    model = ORMOperation
