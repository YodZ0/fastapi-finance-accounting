from src.core.models.period import ORMPeriod
from src.core.repositories import SQLAlchemyRepository


class PeriodsRepository(SQLAlchemyRepository):
    model = ORMPeriod
