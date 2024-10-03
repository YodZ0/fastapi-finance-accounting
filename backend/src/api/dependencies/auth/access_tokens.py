from typing import TYPE_CHECKING, Annotated

from fastapi import Depends

from src.core.models import AccessToken
from src.core.models.database import get_db_helper
from src.loggers import get_logger

if TYPE_CHECKING:
    from src.core.models.database import DataBaseHelper

logger = get_logger(__name__)


async def get_access_tokens_db(
    db_helper: Annotated[
        "DataBaseHelper",
        Depends(get_db_helper),
    ],
):
    async with db_helper.session_factory() as session:
        logger.debug("ACCESS_TOKEN: Session CALLED")
        yield AccessToken.get_db(session)
        logger.debug("ACCESS_TOKEN: Session CLOSED.")
