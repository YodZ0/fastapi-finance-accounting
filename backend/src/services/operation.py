from sqlalchemy.exc import IntegrityError

from src.core.models.user import User
from src.core.schemas.operation import OperationCreate, Operation
from src.utils.unit_of_work import UnitOfWork


class OperationService:
    @staticmethod
    async def create_operation(
        uow: UnitOfWork,
        new_operation: OperationCreate,
        user: User,
    ) -> dict[str, int]:
        operation_dict = new_operation.model_dump()
        operation_dict["user_id"] = user.id
        try:
            async with uow:
                new_operation_id = await uow.operations.add_one(**operation_dict)
                return {"new_operation_id": new_operation_id}
        except IntegrityError:
            raise
        except Exception:
            raise

    @staticmethod
    async def get_all_user_operations(
        uow: UnitOfWork,
        user: User,
    ) -> dict[str, list[Operation]]:
        try:
            async with uow:
                operations: list[Operation] = await uow.operations.get_filtered(
                    user_id=user.id,
                )
                result = [
                    Operation.model_validate(operation) for operation in operations
                ]
                return {"operations": result}
        except IntegrityError:
            raise
        except Exception:
            raise

    @staticmethod
    async def delete_operation(
        uow: UnitOfWork,
        operation_id: int,
        user: User,
    ) -> dict[str, int] | None:
        try:
            async with uow:
                operation = await uow.operations.get_one_by_pk(pk=operation_id)
                if operation:
                    operation = Operation.model_validate(operation)
                    if operation.user_id == user.id:
                        deleted_operation_id = await uow.operations.delete_one(
                            pk=operation_id
                        )
                    return {"deleted_id": deleted_operation_id}
                else:
                    return None
        except Exception:
            raise
