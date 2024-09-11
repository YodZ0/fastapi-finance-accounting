from core.models.role import ORMRole
from core.repositories import SQLAlchemyRepository


class RolesRepository(SQLAlchemyRepository):
    model = ORMRole
