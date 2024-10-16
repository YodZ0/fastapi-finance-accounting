from abc import ABC, abstractmethod
from sqlalchemy.exc import (
    IntegrityError,
    OperationalError,
    DataError,
    ProgrammingError,
    DatabaseError,
)

from src.core.models.database import DataBaseHelper
from src.core.repositories.category import CategoriesRepository
from src.core.repositories.period import PeriodsRepository
from src.loggers import get_logger

logger = get_logger(__name__)


class IUnitOfWork(ABC):
    categories: CategoriesRepository
    periods: PeriodsRepository

    @abstractmethod
    def __init__(self): ...

    @abstractmethod
    async def __aenter__(self): ...

    @abstractmethod
    async def __aexit__(self, *args): ...

    @abstractmethod
    async def commit(self): ...

    @abstractmethod
    async def rollback(self): ...


class UnitOfWork(IUnitOfWork):
    def __init__(self, db_helper: DataBaseHelper):
        self.db_helper = db_helper
        self.session_factory = db_helper.session_factory

    async def __aenter__(self):
        async with self.session_factory() as session:
            self.session = session
            self.categories = CategoriesRepository(self.session)
            self.periods = PeriodsRepository(self.session)
            return self

    async def __aexit__(self, exc_type, exc_value, traceback) -> None:
        try:
            if exc_type is None:
                await self.commit()
            else:
                await self.rollback()
        finally:
            if self.session:
                await self.session.close()
                logger.debug("UOW: Session CLOSED")

    async def commit(self):
        try:
            if self.session:
                await self.session.commit()
                logger.debug("UOW: Session COMMIT")
        except IntegrityError as e:
            await self.rollback()
            logger.warning("UOW: IntegrityError occurred: {ex}", ex=e)
            raise
        except OperationalError as e:
            await self.rollback()
            logger.warning("UOW: OperationalError occurred: {ex}", ex=e)
            raise
        except DataError as e:
            await self.rollback()
            logger.warning("UOW: DataError occurred: {ex}", ex=e)
            raise
        except ProgrammingError as e:
            await self.rollback()
            logger.warning("UOW: ProgrammingError occurred: {ex}", ex=e)
            raise
        except DatabaseError as e:
            await self.rollback()
            logger.warning("UOW: DatabaseError occurred: {ex}", ex=e)
            raise
        except Exception as e:
            await self.rollback()
            logger.warning("UOW: An unexpected error occurred: {ex}", ex=e)
            raise

    async def rollback(self):
        if self.session:
            await self.session.rollback()
            logger.debug("UOW: Session ROLLED BACK")
