from core.schemas import OperationCreate, OperationFilter
from utils.unit_of_work import UnitOfWork


class OperationsService:
    @staticmethod
    async def add_operation(uow: UnitOfWork, operation: OperationCreate):
        operation_dict = operation.model_dump()
        async with uow:
            operation_id = await uow.operations.add_one(data=operation_dict)
            await uow.commit()
            return operation_id

    @staticmethod
    async def get_all_operations(uow: UnitOfWork, offset: int = None, limit: int = None):
        async with uow:
            operations = await uow.operations.find_all(offset=offset, limit=limit)
            return operations

    @staticmethod
    async def filter_operations(uow: UnitOfWork, filters: OperationFilter = None):
        filters_dict = filters.model_dump()
        currency = filters_dict['currency']

        if filters_dict['date_start'] is not None:
            period = {
                'start': filters_dict['date_start'],
                'end': filters_dict['date_end'],
            }
        else:
            period = None
        kind = filters_dict['kind']
        async with uow:
            operations = await uow.operations.filter_all(currency=currency, period=period, kind=kind)
            return operations
