from fastapi import APIRouter, HTTPException, Depends, status

from sqlalchemy.exc import IntegrityError

from src.api.api_v1.dependencies import get_uow
from src.core.schemas.period import PeriodCreate
from src.services.period import PeriodService
from src.loggers import get_logger

from .fast_api_users import current_user

router = APIRouter()
logger = get_logger(__name__)


@router.post(
    "/add",
    status_code=status.HTTP_201_CREATED,
    description="Create new period.",
)
async def create_period(
    new_period: PeriodCreate,
    uow=Depends(get_uow),
    user=Depends(current_user),
):
    try:
        logger.debug("Request: Create new category.")
        new_period_id = await PeriodService().create_period(uow, new_period, user)
        logger.success("Success: New period created (id: {id})", id=new_period_id)
        return {"message": "success", "data": new_period_id}
    except IntegrityError:
        raise HTTPException(status_code=400, detail="IntegrityError")
    except Exception as e:
        logger.error("API: Unexpected error occurred: {ex}", ex=e)
        raise HTTPException(status_code=500, detail="Internal server error.")


@router.get(
    "/all",
    status_code=status.HTTP_200_OK,
    description="Get all user periods.",
)
async def get_all_user_periods(
    uow=Depends(get_uow),
    user=Depends(current_user),
):
    try:
        periods_dict = await PeriodService().get_all_user_periods(uow, user)
        return {"message": "success", "data": periods_dict}
    except Exception as e:
        logger.error("API: Unexpected error occurred: {ex}", ex=e)
        raise HTTPException(status_code=500, detail="Internal server error.")
