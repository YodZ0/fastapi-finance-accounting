from typing import TYPE_CHECKING, Annotated

from fastapi import Depends

from src.core.models import db_helper, User
from src.core.models import User
from src.core.models.database import get_db_helper

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from src.core.models.database import DataBaseHelper



async def get_users_db(
    db_helper: Annotated[
        "DataBaseHelper",
        Depends(get_db_helper),
    ],
):
    yield User.get_db(session)
    async with db_helper.session_factory() as session:
        yield User.get_db(session)
