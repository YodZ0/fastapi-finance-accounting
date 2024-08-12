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
    async def delete_operation(uow: UnitOfWork, operation_id: int) -> int | None:
        async with uow:
            operation_id = await uow.operations.delete_one(_id=operation_id)
            await uow.commit()
            return operation_id

    @staticmethod
    async def delete_multiple_operations(uow: UnitOfWork, operations_ids: list[int]) -> list[int]:
        async with uow:
            operations_ids = await uow.operations.delete_multiple(ids=operations_ids)
            await uow.commit()
            return operations_ids

    @staticmethod
    async def get_all_operations(uow: UnitOfWork, limit: int = None, offset: int = None):
        async with uow:
            operations = await uow.operations.find_all(limit=limit, offset=offset)
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
        category = filters_dict['category']
        async with uow:
            operations = await uow.operations.filter_all(
                currency=currency,
                period=period,
                kind=kind,
                category=category
            )
            return operations
