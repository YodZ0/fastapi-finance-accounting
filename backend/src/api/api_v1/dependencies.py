from typing import Annotated, TYPE_CHECKING

from fastapi import Depends

from src.utils.unit_of_work import IUnitOfWork, UnitOfWork
from src.core.models.database import get_db_helper
from src.utils.unit_of_work import UnitOfWork

if TYPE_CHECKING:
    from src.core.models.database import DataBaseHelper

UOWDep = Annotated[IUnitOfWork, Depends(UnitOfWork)]
def get_uow(
    db_helper: Annotated["DataBaseHelper", Depends(get_db_helper)]
) -> UnitOfWork:
    return UnitOfWork(db_helper)
