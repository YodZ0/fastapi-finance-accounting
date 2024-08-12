from fastapi import APIRouter

from core.schemas import OperationRead, OperationCreate, OperationFilter
from services.operations import OperationsService
from core.schemas import OperationRead, OperationCreate, OperationFilter
from .dependencies import UOWDep

# api_v1 url = ..api/v1/operations/
router = APIRouter()


@router.post('/add')
async def add_operation(
        uow: UOWDep,
        operation: OperationCreate,
) -> dict:
    operation_id = await OperationsService().add_operation(uow, operation)
    return {'operation_id': str(operation_id), 'message': 'Created', 'status_code': '201'}


@router.delete('/delete/{operation_id}')
async def delete_operation(uow: UOWDep, operation_id: int) -> dict:
    operation_id = await OperationsService().delete_operation(uow, operation_id=operation_id)
    if operation_id is not None:
        return {'deleted': str(operation_id), 'status_code': '200'}
    else:
        return {'message': 'Operation not found', 'status_code': '404'}


@router.post('/delete-multiple')
async def delete_multiple_operations(uow: UOWDep, operations_ids: list[int]) -> dict:
    operations_ids = await OperationsService().delete_multiple_operations(uow, operations_ids=operations_ids)
    if operations_ids:
        return {'deleted': str(operations_ids), 'status_code': '200'}
    else:
        return {'message': 'Operations not found', 'status_code': '404'}


@router.get('', response_model=list[OperationRead])
async def get_all_operations(
        uow: UOWDep,
        limit: int = None,
        offset: int = None,
        limit: int = None,
) -> list[OperationRead]:
    operations = await OperationsService().get_all_operations(uow, limit=limit, offset=offset)
    return operations


@router.get('/filter', response_model=list[OperationRead])
async def filter_operations(
        uow: UOWDep,
        currency: str = None,
        kind: str = None,
        category: str = None,
        date_start: str = None,
        date_end: str = None,
) -> list[OperationRead]:
    filters = OperationFilter(
        currency=currency,
        kind=kind,
        category=category,
        date_start=date_start,
        date_end=date_end
    )
    operations = await OperationsService().filter_operations(uow, filters)
    return operations


@router.get('/diagrams')
async def get_diagram_data(
        uow: UOWDep,
        currency: str = None,
        date_start: str = None,
        date_end: str = None,
) -> dict:
    filters = OperationFilter(
        currency=currency,
        date_start=date_start,
        date_end=date_end
    )
    diagram_data = await OperationsService().get_diagram_data(uow, filters)
    return diagram_data
