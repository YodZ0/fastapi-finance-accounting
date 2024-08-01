from fastapi import APIRouter

from services.operations import OperationsService
from core.schemas import OperationRead, OperationCreate
from .dependencies import UOWDep

router = APIRouter()


@router.get('')
async def get_operations(
        uow: UOWDep,
) -> list[OperationRead]:
    operations = await OperationsService().get_operations(uow)
    return operations


@router.post('')
async def add_operation(
        operation: OperationCreate,
        uow: UOWDep,
) -> dict:
    operation_id = await OperationsService().add_operation(uow, operation)
    return {'operation_id': str(operation_id), 'status': '201', 'message': 'Created'}
