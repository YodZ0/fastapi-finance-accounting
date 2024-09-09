from sqlalchemy.exc import IntegrityError

from .schemas import CategoryCreate, Category, CategoryType
from utils.unit_of_work import UnitOfWork


class CategoryService:
    @staticmethod
    async def generate_categories(
            uow: UnitOfWork,
    ):
        categories_list = [
            CategoryCreate(name='Food', type='Expense').model_dump(),
            CategoryCreate(name='Housing', type='Expense').model_dump(),
            CategoryCreate(name='Transport', type='Expense').model_dump(),
            CategoryCreate(name='Internet', type='Expense').model_dump(),
            CategoryCreate(name='Health', type='Expense').model_dump(),
            CategoryCreate(name='Vacation', type='Expense').model_dump(),
            CategoryCreate(name='Other', type='Expense').model_dump(),

            CategoryCreate(name='Salary', type='Income').model_dump(),
            CategoryCreate(name='Bonus', type='Income').model_dump(),
            CategoryCreate(name='Passive', type='Income').model_dump(),
            CategoryCreate(name='Side', type='Income').model_dump(),
            CategoryCreate(name='Gift', type='Income').model_dump(),

            CategoryCreate(name='Investment', type='Investment').model_dump(),
            CategoryCreate(name='Saving', type='Saving').model_dump(),
        ]
        async with uow:
            await uow.categories.add_multiple(data=categories_list)
            await uow.commit()

    @staticmethod
    async def create_category(
            uow: UnitOfWork,
            new_category: CategoryCreate,
    ):
        category_dict = new_category.model_dump()
        try:
            async with uow:
                category_id = await uow.categories.add_one(data=category_dict)
                await uow.commit()
                return category_id
        except IntegrityError:
            raise

    @staticmethod
    async def get_all_categories(
            uow: UnitOfWork,
    ) -> dict[str, list[Category]]:
        try:
            async with uow:
                categories = await uow.categories.get_all()
                expense_cats = []
                income_cats = []
                invest_cats = []
                saving_cats = []
                for cat in categories:
                    category = Category.from_orm(cat)
                    if category.type == CategoryType.EXPENSE:
                        expense_cats.append(category)
                    elif category.type == CategoryType.INCOME:
                        income_cats.append(category)
                    elif category.type == CategoryType.INVESTMENT:
                        invest_cats.append(category)
                    elif category.type == CategoryType.SAVING:
                        saving_cats.append(category)
                return {
                    'Expenses': expense_cats,
                    'Incomes': income_cats,
                    'Investments': invest_cats,
                    'Savings': saving_cats
                }
        except Exception:
            raise

    @staticmethod
    async def delete_category(
            uow: UnitOfWork,
            cat_id: int,
    ) -> int | None:
        async with uow:
            deleted_cat = await uow.categories.delete_one(_id=cat_id)
            await uow.commit()
            return deleted_cat
