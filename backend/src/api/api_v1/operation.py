from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import JSONResponse

from sqlalchemy.exc import IntegrityError

from src.api.api_v1.dependencies import get_uow
from src.core.schemas.operation import OperationCreate
from src.services.operation import OperationService
from src.loggers import get_logger

from .fast_api_users import current_user

router = APIRouter()
logger = get_logger(__name__)


@router.post(
    "/add",
    status_code=status.HTTP_201_CREATED,
    description="Create new operation.",
)
async def create_operation(
    new_operation: OperationCreate,
    uow=Depends(get_uow),
    user=Depends(current_user),
):
    try:
        logger.debug("Request: Create new operation.")
        new_operation_id = await OperationService().create_operation(
            uow, new_operation, user
        )
        logger.success("Success: New operation created (id: {id})", id=new_operation_id)
        return {"message": "success", "data": new_operation_id}
    except IntegrityError:
        raise HTTPException(status_code=400, detail="IntegrityError")
    except Exception as e:
        logger.error("API: Unexpected error occurred: {ex}", ex=e)
        raise HTTPException(status_code=500, detail="Internal server error.")


@router.get(
    "/all",
    status_code=status.HTTP_200_OK,
    description="Get all user operations.",
)
async def get_all_user_operations(
    uow=Depends(get_uow),
    user=Depends(current_user),
):
    try:
        operations_dict = await OperationService().get_all_user_operations(uow, user)
        return {"message": "success", "data": operations_dict}
    except Exception as e:
        logger.error("API: Unexpected error occurred: {ex}", ex=e)
        raise HTTPException(status_code=500, detail="Internal server error.")


@router.delete(
    "/delete/{operation_id}",
    status_code=status.HTTP_200_OK,
    description="Delete the operation.",
)
async def delete_operation(
    operation_id: int,
    uow=Depends(get_uow),
    user=Depends(current_user),
):
    try:
        deleted_id = await OperationService().delete_operation(uow, operation_id, user)

        if deleted_id is not None:
            return {"message": "success", "data": deleted_id}

        return JSONResponse(
            status_code=404,
            content="Object not found.",
        )
    except IntegrityError:
        raise HTTPException(status_code=400, detail="IntegrityError")
    except Exception as e:
        logger.error("API: Unexpected error occurred: {ex}", ex=e)
        raise HTTPException(status_code=500, detail="Internal server error.")
