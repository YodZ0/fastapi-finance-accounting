from fastapi import APIRouter

from services.operations import OperationsService
from core.schemas import OperationRead, OperationCreate, OperationFilter
from .dependencies import UOWDep

# api_v1 url = ..api/v1/operations/
router = APIRouter()


@router.post('')
async def add_operation(
        uow: UOWDep,
        operation: OperationCreate,
) -> dict:
    operation_id = await OperationsService().add_operation(uow, operation)
    return {'operation_id': str(operation_id), 'status': '201', 'message': 'Created'}


@router.get('')
async def get_all_operations(
        uow: UOWDep,
        offset: int = None,
        limit: int = None,
) -> list[OperationRead]:
    operations = await OperationsService().get_all_operations(uow, offset=offset, limit=limit)
    return operations


@router.get('/filter')
async def filter_operations(
        uow: UOWDep,
        currency: str = None,
        kind: str = None,
        date_start: str = None,
        date_end: str = None,
):
    filters = OperationFilter(
        currency=currency,
        kind=kind,
        date_start=date_start,
        date_end=date_end
    )
    operations = await OperationsService().filter_operations(uow, filters)
    return operations
