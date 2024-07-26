from abc import ABC, abstractmethod

from sqlalchemy.sql import select
from sqlalchemy.dialects.postgresql import insert

from core.models.database import async_session_maker


class AbstractRepository(ABC):

    @abstractmethod
    async def add_one(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def find_all(self, *args, **kwargs):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    async def add_one(self, data: dict):
        async with async_session_maker() as session:
            # stmt = insert(self.model).values(**data).returning(self.model.id)
            stmt = insert(self.model).values(**data)
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar_one()

    async def find_all(self, **order_by):
        async with async_session_maker() as session:
            stmt = select(self.model).order_by(self.model.id.desc())
            result = await session.execute(stmt)
            result = [row[0].to_read_model() for row in result.all()]
            return result
