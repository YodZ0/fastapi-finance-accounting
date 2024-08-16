from datetime import datetime
from collections import defaultdict

from fastapi.responses import FileResponse

from core.config import settings
from core.schemas import OperationCreate, OperationFilter, OperationBase, OperationRead

from utils.file_handler import read_line_from_txt_file, read_from_csv, write_to_csv
from utils.unit_of_work import UnitOfWork


class OperationsService:
    @staticmethod
    async def add_operation(
            uow: UnitOfWork,
            operation: OperationCreate,
    ) -> int:
        """
        Adds a new operation to the database.

        Args:
            uow (UnitOfWork): The unit of work context that manages transactions.
            operation (OperationCreate): The operation data schema containing all necessary fields.

        Returns:
            int: The ID of the created operation in the database.
        """
        operation_dict = operation.model_dump()
        async with uow:
            operation_id = await uow.operations.add_one(data=operation_dict)
            await uow.commit()
            return operation_id

    @staticmethod
    async def add_multiple_operations(
            uow: UnitOfWork,
            operations: list[OperationCreate],
    ) -> list[int]:
        """
        Adds multiple operations to the database.

        Args:
            uow (UnitOfWork): The unit of work context that manages transactions.
            operations (list[OperationCreate]): A list of operation data schemas, each containing all necessary fields.

        Returns:
            list[int]: A list of IDs corresponding to the newly created operations in the database.
        """
        data = [operation.model_dump() for operation in operations]
        async with uow:
            operations_ids = await uow.operations.add_multiple(data=data)
            await uow.commit()
            return operations_ids

    @staticmethod
    async def delete_operation(
            uow: UnitOfWork,
            operation_id: int,
    ) -> int | None:
        """
        Deletes an operation from the database by its ID.

        Args:
            uow (UnitOfWork): The unit of work context that manages transactions.
            operation_id (int): The ID of the operation to be deleted.

        Returns:
            int | None: The ID of the deleted operation if successful, otherwise None.
        """
        async with uow:
            operation_id = await uow.operations.delete_one(_id=operation_id)
            await uow.commit()
            return operation_id

    @staticmethod
    async def delete_multiple_operations(
            uow: UnitOfWork,
            operations_ids: list[int],
    ) -> list[int]:
        """
        Deletes multiple operations from the database by their IDs.

        Args:
            uow (UnitOfWork): The unit of work context that manages transactions.
            operations_ids (list[int]): A list of IDs of the operations to be deleted.

        Returns:
            list[int]: A list of IDs of the successfully deleted operations.
        """
        async with uow:
            operations_ids = await uow.operations.delete_multiple(ids=operations_ids)
            await uow.commit()
            return operations_ids

    @staticmethod
    async def get_all_operations(
            uow: UnitOfWork,
            limit: int = None,
            offset: int = None,
    ) -> list[OperationRead]:
        """
        Fetching ALL operations from database.

        Args:
            uow (UnitOfWork): The unit of work context that manages transactions.
            limit (int, optional): The maximum number of operations to retrieve.
            offset (int, optional): The number of operations to skip before starting to collect results.

        Returns:
            list[OperationRead]: A list of operations retrieved from the database.
        """
        async with uow:
            operations = await uow.operations.find_all(limit=limit, offset=offset)
            return operations

    @staticmethod
    async def filter_operations(
            uow: UnitOfWork,
            filters: OperationFilter = None,
    ) -> list[OperationRead]:
        """
        Filters operations based on the provided filter criteria.

        Args:
            uow (UnitOfWork): The unit of work context that manages transactions.
            filters (OperationFilter, optional): An object containing filter criteria such as currency,
                date range, kind, and category.

        Returns:
            list[OperationRead]: A list of operations that match the filter criteria.
        """
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
    async def get_diagram_data(
            uow: UnitOfWork,
            filters: OperationFilter = None,
    ) -> dict:
        """
        Filters operations based on the provided criteria and summarizes the total amounts
        for incomes and expenses by category.

        Args:
            uow (UnitOfWork): The unit of work context that manages transactions.
            filters (OperationFilter, optional): An object containing filter criteria: currency, data range.

        Returns:
            dict: A dictionary containing the summarized data for incomes and expenses, including:
            - 'incomes': A dictionary with the total income amount and breakdown by category.
            - 'expenses': A dictionary with the total expense amount and breakdown by category.
            - 'proportions': A dictionary with the percentage proportions of incomes and expenses relative to the total.
        """
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
                    {'category': item, 'value': round(value, 2)}
                )
            total_exp = 0
            for item, value in exp_cat_amount_dict.items():
                total_exp += value
                expenses_values.append(
                    {'category': item, 'value': round(value, 2)}
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
                        {'category': '% Incomes', 'value': inc_proportion},
                        {'category': '% Expenses', 'value': exp_proportion},
                    ],
                },
            }
            return data

    @staticmethod
    async def create_operations_from_file(
            uow: UnitOfWork,
            file,
            file_format: str,
    ) -> list[int] | None:
        """
        Creates operations in the database from a file.
        ** Allowed formats: .txt, .csv.

        Args:
            uow (UnitOfWork): The unit of work context that manages transactions.
            file: The file object to read operation data from.
            file_format (str): The format of the file.

        Returns:
            list[int] | None: A list of IDs of the newly created operations if the file format is supported,
            otherwise None.
        """
        file_location = settings.media_dir / 'import' / file.filename

        async with uow:
            # Save the file locally
            with open(file_location, 'wb') as f:
                f.write(await file.read())

            if file_format == 'csv':
                # Read and process CSV file
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
            # elif file_format == 'plain':
            #     # Read and process TXT file
            #     # gen = read_line_from_txt_file(file_location)
            #     # await uow.commit()
            #     return operations_ids
            else:
                return None

    @staticmethod
    async def send_operations_csv_file(
            uow: UnitOfWork,
            filters: OperationFilter = None,
    ) -> FileResponse:
        """
        Generates and returns a CSV file of operations based on provided filters.

        Args:
            uow (UnitOfWork): The unit of work context that manages transactions.
            filters (OperationFilter, optional): An object containing filter criteria: currency, date range.

        Returns:
            FileResponse: A response containing the CSV file for download, including its path, filename, and media type.
        """
        filters_dict = filters.model_dump()
        currency = filters_dict['currency']

        if filters_dict['date_start'] is not None:
            period = {
                'start': filters_dict['date_start'],
                'end': filters_dict['date_end'],
            }
            filename = f'export_{period['start']}__{period['end']}_{currency}.csv'
        else:
            period = None
            filename = f'export_all_operations_{currency}.csv'

        file_location = settings.media_dir / 'export' / filename

        async with uow:
            operations: list[OperationBase] = await uow.operations.filter_all(
                currency=currency,
                period=period,
            )
            data = [operation.model_dump() for operation in operations]
            write_to_csv(data, file_location)

        return FileResponse(path=file_location, filename=filename, media_type='multipart/form-data')
