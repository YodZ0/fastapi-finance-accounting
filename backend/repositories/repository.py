from abc import ABC, abstractmethod

from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert


class AbstractRepository(ABC):

    @abstractmethod
    async def add_one(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def find_all(self, *args, **kwargs):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_one(self, data: dict) -> int:
        stmt = insert(self.model).values(**data).returning(self.model.id)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def edit_one(self, _id: int, data: dict) -> int:
        stmt = update(self.model).values(**data).filter_by(id=_id).returning(self.model.id)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def find_one(self, **filter_by):
        stmt = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(stmt)
        res = res.scalar_one().to_read_model()
        return res

    async def find_all(self, offset: int = None, limit: int = None):
        stmt = select(self.model).offset(offset).limit(limit)
        res = await self.session.execute(stmt)
        res = [row[0].to_read_model() for row in res.all()]
        return res

    async def filter_all(
            self, currency: str = None,
            period: dict[str, str] = None,
            kind: str = None,
            category: str = None,
    ):
        stmt = select(self.model)

        if currency is not None:
            stmt = stmt.where(self.model.currency == currency)
        if period is not None:
            stmt = stmt.filter(self.model.date.between(period['start'], period['end']))
        if kind is not None:
            stmt = stmt.where(self.model.kind == kind)
        if category is not None:
            stmt = stmt.where(self.model.category == category)

        result = await self.session.execute(stmt)
        res = [row[0].to_read_model() for row in result.all()]
        return res
