from typing import Annotated, TYPE_CHECKING

from fastapi import Depends

from src.core.models.database import get_db_helper
from src.loggers import get_logger
from src.utils.unit_of_work import UnitOfWork

if TYPE_CHECKING:
    from src.core.models.database import DataBaseHelper

logger = get_logger(__name__)


def get_uow(
    db_helper: Annotated["DataBaseHelper", Depends(get_db_helper)]
) -> UnitOfWork:
    logger.debug("UOW DEP: Call DB_HELPER")
    return UnitOfWork(db_helper)
