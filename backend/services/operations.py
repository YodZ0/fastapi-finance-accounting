from core.schemas import OperationCreate
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
    async def get_operations(uow: UnitOfWork):
        async with uow:
            operations = await uow.operations.find_all()
            return operations
