from abc import ABC, abstractmethod
from sqlalchemy.exc import IntegrityError, OperationalError, DataError, ProgrammingError, DatabaseError

from core.models.database import async_session_maker

from modules.categories.repository import CategoriesRepository
from modules.roles.repository import RolesRepository


class IUnitOfWork(ABC):
    categories: CategoriesRepository
    roles: RolesRepository

    @abstractmethod
    def __init__(self):
        ...

    @abstractmethod
    async def __aenter__(self):
        ...

    @abstractmethod
    async def __aexit__(self, *args):
        ...

    @abstractmethod
    async def commit(self):
        ...

    @abstractmethod
    async def rollback(self):
        ...


class UnitOfWork(IUnitOfWork):
    def __init__(self):
        self.session_factory = async_session_maker

    async def __aenter__(self):
        async with self.session_factory() as session:
            self.session = session
            self.categories = CategoriesRepository(self.session)
            self.roles = RolesRepository(self.session)
            return self

    async def __aexit__(self, exc_type, exc_value, traceback) -> None:
        if exc_type is None:
            await self.commit()
        else:
            await self.rollback()
        await self.session.close()

    async def commit(self):
        try:
            if self.session:
                await self.session.commit()
        except IntegrityError as e:
            await self.rollback()
            print(f'IntegrityError occurred: {e}')
            raise
        except OperationalError as e:
            await self.rollback()
            print(f'OperationalError occurred: {e}')
            raise
        except DataError as e:
            await self.rollback()
            print(f'DataError occurred: {e}')
            raise
        except ProgrammingError as e:
            await self.rollback()
            print(f'ProgrammingError occurred: {e}')
            raise
        except DatabaseError as e:
            await self.rollback()
            print(f'DatabaseError occurred: {e}')
            raise
        except Exception as e:
            await self.rollback()
            print(f'An unexpected error occurred: {e}')
            raise

    async def rollback(self):
        if self.session:
            await self.session.rollback()
