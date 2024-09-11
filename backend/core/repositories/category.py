from core.models.category import ORMCategory
from core.repositories import SQLAlchemyRepository


class CategoriesRepository(SQLAlchemyRepository):
    model = ORMCategory
