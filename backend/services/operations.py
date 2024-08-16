from datetime import datetime

from fastapi.responses import FileResponse

from core.config import settings
from core.schemas import OperationCreate, OperationFilter, OperationBase

from utils.file_handler import read_line_from_txt_file, read_from_csv, write_to_csv
from utils.unit_of_work import UnitOfWork

from collections import defaultdict


class OperationsService:
    @staticmethod
    async def add_operation(uow: UnitOfWork, operation: OperationCreate):
        operation_dict = operation.model_dump()
        async with uow:
            operation_id = await uow.operations.add_one(data=operation_dict)
            await uow.commit()
            return operation_id

    @staticmethod
    async def add_multiple_operations(uow: UnitOfWork, operations: list[OperationCreate]):
        data = [operation.model_dump() for operation in operations]
        async with uow:
            operations_ids = await uow.operations.add_multiple(data=data)
            await uow.commit()
            return operations_ids

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
                    {'type': item, 'value': round(value, 2)}
                )

            total_exp = 0
            for item, value in exp_cat_amount_dict.items():
                total_exp += value
                expenses_values.append(
                    {'type': item, 'value': round(value, 2)}
                )

            total = total_inc + total_exp
            if total != 0:
                inc_proportion = round(total_inc * 100 / total, 2)
                exp_proportion = round(total_exp * 100 / total, 2)
            else:
                inc_proportion = 0
                exp_proportion = 0

            data = {
                'incomes': {
                    'title': f'Income, {filters.currency.name}\n{round(total_inc, 2)}',
                    'values': incomes_values,
                },
                'expenses': {
                    'title': f'Expense, {filters.currency.name}\n{round(total_exp, 2)}',
                    'values': expenses_values,
                },
                'proportions': {
                    'title': f'% Total, {filters.currency.name}',
                    'values': [
                        {'type': '% Incomes', 'value': inc_proportion},
                        {'type': '% Expenses', 'value': exp_proportion},
                    ],
                },
            }

            return data

    @staticmethod
    async def create_operations_from_file(uow: UnitOfWork, file, file_format):
        file_location = settings.media_dir / 'import' / file.filename

        async with uow:
            with open(file_location, 'wb') as f:
                f.write(await file.read())

            if file_format == 'csv':
                gen = read_from_csv(file_location)
                new_operations = []
                for line in gen:
                    if 'id' in line:
                        del line['id']

                    line['amount'] = float(line['amount'])
                    line['date'] = datetime.strptime(line['date'], '%d.%m.%Y').date()
                    new_operations.append(line)

                operations_ids = await uow.operations.add_multiple(data=new_operations)
                await uow.commit()
                return operations_ids
            elif file_format == 'plain':
                gen = read_line_from_txt_file(file_location)
            else:
                return None

    @staticmethod
    async def send_operations_csv_file(uow: UnitOfWork, filters: OperationFilter = None) -> FileResponse:
        filters_dict = filters.model_dump()
        currency = filters_dict['currency']

        if filters_dict['date_start'] is not None:
            period = {
                'start': filters_dict['date_start'],
                'end': filters_dict['date_end'],
            }
            filename = f'Operations__{period['start']}__{period['end']}.csv'
        else:
            period = None
            filename = f'All__operations.csv'

        file_location = settings.media_dir / 'export' / filename

        async with uow:
            operations: list[OperationBase] = await uow.operations.filter_all(
                currency=currency,
                period=period,
            )
            data = [operation.model_dump() for operation in operations]
            write_to_csv(data, file_location)

        return FileResponse(path=file_location, filename=filename, media_type='multipart/form-data')
