from typing import TYPE_CHECKING, Annotated

from fastapi import Depends

from src.core.models import db_helper, AccessToken
from src.loggers import get_logger

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
logger = get_logger(__name__)


async def get_access_tokens_db(
    session: Annotated[
        "AsyncSession",
        Depends(db_helper.session_getter),
    ],
):
    yield AccessToken.get_db(session)
        logger.debug("ACCESS_TOKEN: Session CALLED")
        logger.debug("ACCESS_TOKEN: Session CLOSED.")
