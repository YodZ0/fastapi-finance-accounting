from .repository import AbstractRepository

from sqlalchemy import insert, select, update, delete
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession


class SQLAlchemyRepository(AbstractRepository):
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_one(self, data: dict) -> int:
        stmt = insert(self.model).values(**data).returning(self.model.id)
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def add_multiple(self, data: list[dict]) -> list[int]:
        stmt = insert(self.model).values(data).returning(self.model.id)
        result = await self.session.execute(stmt)
        res = [row[0] for row in result.all()]
        return res

    async def edit_one(self, _id: int, data: dict) -> int | None:
        stmt = (
            update(self.model).values(**data).filter_by(id=_id).returning(self.model.id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def delete_one(self, _id: int) -> int | None:
        stmt = delete(self.model).filter_by(id=_id).returning(self.model.id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def delete_multiple(self, ids: list[int]) -> list[int]:
        stmt = delete(self.model).where(self.model.id.in_(ids)).returning(self.model.id)
        result = await self.session.execute(stmt)
        res = [row[0] for row in result.all()]
        return res

    async def get_by_id(self, _id: int, *, load_related: bool = False):
        query = select(self.model).filter_by(id=_id)
        if load_related:
            related_fields = self.model.get_related_fields()
            for field in related_fields:
                query = query.options(joinedload(field))
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_one_filtered(self, **filters):
        query = select(self.model)

        for key, value in filters.items():
            if value is not None and hasattr(self.model, key):
                query = query.where(getattr(self.model, key) == value)

        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_all(self, *, load_related: bool = False):
        query = select(self.model)
        if load_related:
            related_fields = self.model.get_related_fields()
            for field in related_fields:
                query = query.options(joinedload(field))
        result = await self.session.execute(query)
        res = result.scalars().all()
        return res

    async def get_all_filtered(self, *, load_options: bool = False, **filters):
        query = select(self.model)

        if load_options:
            related_fields = self.model.get_related_fields()
            for field in related_fields:
                query = query.options(joinedload(field))

        if filters:
            for key, value in filters.items():
                if value is not None and hasattr(self.model, key):
                    query = query.where(getattr(self.model, key) == value)

        result = await self.session.execute(query)
        res = result.scalars().all()
        return res
