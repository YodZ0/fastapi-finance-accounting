from core.schemas import OperationCreate, OperationRead, OperationBase
from repositories import OperationsRepository


class OperationsService:
    def __init__(self, operations_repo: type(OperationsRepository)):
        self.operations_repo: OperationsRepository = operations_repo()

    async def add_operation(self, operation: OperationCreate):
        operation_dict = operation.model_dump()
        operation_id = await self.operations_repo.add_one(operation_dict)
        return operation_id

    async def get_operations(self, **order_by):
        operations = await self.operations_repo.find_all(**order_by)
        return operations
