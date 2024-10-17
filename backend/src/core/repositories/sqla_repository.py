from typing import Any

from .repository import AbstractRepository

from sqlalchemy import insert, select, delete
from sqlalchemy.ext.asyncio import AsyncSession


class SQLAlchemyRepository(AbstractRepository):
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_one(self, **values) -> int:
        stmt = insert(self.model).values(values).returning(self.model.id)
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def edit_one(self):
        pass

    async def delete_one(self, pk: int) -> int | None:
        stmt = delete(self.model).filter_by(id=pk).returning(self.model.id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_one_by_pk(self, pk) -> Any | None:
        query = select(self.model).filter_by(id=pk)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_all(self):
        query = select(self.model)
        result = await self.session.execute(query)
        res = result.scalars().all()
        return res

    async def get_filtered(self, **filters):
        query = select(self.model)

        if filters:
            for key, value in filters.items():
                if value is not None and hasattr(self.model, key):
                    query = query.where(getattr(self.model, key) == value)

        result = await self.session.execute(query)
        res = result.scalars().all()
        return res
