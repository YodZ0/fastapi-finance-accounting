from src.core.models.category import ORMCategory
from src.core.repositories import SQLAlchemyRepository


class CategoriesRepository(SQLAlchemyRepository):
    model = ORMCategory
