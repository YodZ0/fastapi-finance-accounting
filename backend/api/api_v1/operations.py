import datetime
from typing import Annotated

from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse

from core.schemas import OperationRead, OperationCreate, OperationFilter
from core.schemas.operations import Currency, OperationKind, IncomeCategories, ExpenseCategories
from services.operations import OperationsService
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
async def delete_operation(
        uow: UOWDep,
        operation_id: int
) -> dict:
    operation_id = await OperationsService().delete_operation(uow, operation_id=operation_id)
    if operation_id is not None:
        return {'deleted': str(operation_id), 'status_code': '200'}
    else:
        return {'message': 'Operation not found', 'status_code': '404'}


@router.post('/delete-multiple')
async def delete_multiple_operations(
        uow: UOWDep,
        operations_ids: list[int]
) -> dict:
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
) -> list[OperationRead]:
    operations = await OperationsService().get_all_operations(uow, limit=limit, offset=offset)
    return operations


@router.get('/filter', response_model=list[OperationRead])
async def filter_operations(
        uow: UOWDep,
        currency: Currency = None,
        kind: OperationKind = None,
        category: str = None,
        date_start: datetime.date = None,
        date_end: datetime.date = None,
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
        currency: Currency,
        date_start: datetime.date = None,
        date_end: datetime.date = None,
) -> dict:
    filters = OperationFilter(
        currency=currency,
        date_start=date_start,
        date_end=date_end
    )
    diagram_data = await OperationsService().get_diagram_data(uow, filters)
    return diagram_data


@router.post('/file')
async def upload_file(
        uow: UOWDep,
        file: Annotated[UploadFile, File(description='Allowed formats: .txt, .csv')]
):
    allowed_formats = ['csv', 'plain']
    file_format = file.headers['content-type'].split('/')[1]

    if file_format in allowed_formats:
        operations_ids = await OperationsService().create_operations_from_file(uow, file, file_format)
        return {'created': str(operations_ids), 'status_code': '201'}
    else:
        return HTTPException(status_code=403, detail=f"Invalid file format: '{file_format}'. Allowed: .csv, .txt")


@router.get('/file/download', response_description='Download operations csv file.')
async def download_csv_file(
        uow: UOWDep,
        currency: Currency = None,
        date_start: datetime.date = None,
        date_end: datetime.date = None,
) -> FileResponse:
    filters = OperationFilter(
        currency=currency,
        date_start=date_start,
        date_end=date_end
    )
    file = await OperationsService().send_operations_csv_file(uow, filters)
    return file
