from typing import Annotated

from fastapi import APIRouter, Depends

from services.operations import OperationsService
from core.schemas import OperationRead, OperationCreate
from .dependencies import operations_service

router = APIRouter()


@router.get('')
async def get_operations_list(
        service: Annotated[OperationsService, Depends(operations_service)],
) -> list[OperationRead]:
    operations = await service.get_operations()
    return operations


@router.post('')
async def add_new_operation(
        operation: OperationCreate,
        service: Annotated[OperationsService, Depends(operations_service)],
):
    operation_id = await service.add_operation(operation)
    return {'operation_id': operation_id}
