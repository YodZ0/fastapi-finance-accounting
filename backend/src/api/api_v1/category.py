from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import JSONResponse

from sqlalchemy.exc import IntegrityError

from src.api.api_v1.dependencies import get_uow
from src.core.schemas.category import CategoryCreate
from src.services.category import CategoryService
from src.loggers import get_logger

from .fast_api_users import current_user, current_superuser

router = APIRouter()
logger = get_logger(__name__)


@router.post(
    "/add",
    status_code=status.HTTP_201_CREATED,
    description="Create new category.",
    dependencies=[Depends(current_superuser)],
)
async def create_category(
    new_category: CategoryCreate,
    uow=Depends(get_uow),
):
    try:
        logger.debug("Request: Create new category.")
        new_cat_id = await CategoryService().create_category(uow, new_category)
        logger.success("Success: New category created (id: {id})", id=new_cat_id)
        return {"message": "success", "data": new_cat_id}
    except IntegrityError:
        raise HTTPException(
            status_code=400, detail="Category name must be unique. Try another name."
        )
    except Exception as e:
        logger.error("API: Unexpected error occurred: {ex}", ex=e)
        raise HTTPException(status_code=500, detail="Internal server error.")


@router.get(
    "/all",
    status_code=status.HTTP_200_OK,
    description="Get all categories, grouped by their types: INCOMES, EXPENSES, INVESTMENTS, SAVINGS.",
    dependencies=[Depends(current_user)],
)
async def get_all_categories(
    uow=Depends(get_uow),
):
    try:
        categories_dict = await CategoryService().get_all_categories(uow)
        return {"message": "success", "data": categories_dict}
    except Exception as e:
        logger.error("API: Unexpected error occurred: {ex}", ex=e)
        raise HTTPException(status_code=500, detail="Internal server error.")


@router.delete(
    "/delete/{cat_id}",
    status_code=status.HTTP_200_OK,
    description="Delete the category.",
    dependencies=[Depends(current_superuser)],
)
async def delete_category(
    cat_id: int,
    uow=Depends(get_uow),
):
    try:
        deleted_id = await CategoryService().delete_category(uow, cat_id)

        if deleted_id is not None:
            return {"message": "success", "data": deleted_id}

        return JSONResponse(
            status_code=404,
            content="Object not found.",
        )
    except Exception as e:
        logger.error("API: Unexpected error occurred: {ex}", ex=e)
        raise HTTPException(status_code=500, detail="Internal server error.")
