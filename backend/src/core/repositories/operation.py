from src.core.models.operation import ORMOperation
from src.core.repositories import SQLAlchemyRepository


class OperationsRepository(SQLAlchemyRepository):
    model = ORMOperation
