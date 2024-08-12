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

    @staticmethod
    async def get_diagram_data(uow: UnitOfWork, filters: OperationFilter = None):
        filters_dict = filters.model_dump()
        currency = filters_dict['currency']

        if filters_dict['date_start'] is not None:
            period = {
                'start': filters_dict['date_start'],
                'end': filters_dict['date_end'],
            }
        else:
            period = None

        async with uow:
            inc_cat_amount_dict = defaultdict(float)
            exp_cat_amount_dict = defaultdict(float)
            operations: list[OperationBase] = await uow.operations.filter_all(
                currency=currency,
                period=period,
            )

            incomes_values = []
            expenses_values = []
            for operation in operations:
                if operation.kind.name == 'INCOME':
                    inc_cat_amount_dict[operation.category.name] += operation.amount
                else:
                    exp_cat_amount_dict[operation.category.name] += operation.amount

            total_inc = 0
            for item, value in inc_cat_amount_dict.items():
                total_inc += value
                incomes_values.append(
                    {'type': item, 'value': value}
                )

            total_exp = 0
            for item, value in exp_cat_amount_dict.items():
                total_exp += value
                expenses_values.append(
                    {'type': item, 'value': value}
                )

            data = {
                'incomes': {
                    'title': f'Income, {filters.currency.name}\n{total_inc}',
                    'values': incomes_values,
                },
                'expenses': {
                    'title': f'Expense, {filters.currency.name}\n{total_exp}',
                    'values': expenses_values,
                },
            }

            return data
