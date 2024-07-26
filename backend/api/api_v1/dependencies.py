from repositories.operations import OperationsRepository
from services.operations import OperationsService


async def operations_service():
    return OperationsService(OperationsRepository)
