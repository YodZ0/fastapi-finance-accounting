from sqlalchemy.exc import IntegrityError

from src.core.schemas.category import CategoryCreate, Category
from src.utils.unit_of_work import UnitOfWork


class CategoryService:
    @staticmethod
    async def create_category(
        uow: UnitOfWork,
        new_category: CategoryCreate,
    ) -> dict[str, int] | None:
        category_dict = new_category.model_dump()
        try:
            async with uow:
                new_category_id = await uow.categories.add_one(data=category_dict)
                return {"new_category_id": new_category_id}
        except IntegrityError:
            raise
        except Exception:
            raise

    @staticmethod
    async def get_all_categories(
        uow: UnitOfWork,
    ) -> dict[str, dict[str, list[str]]]:
        try:
            async with uow:
                categories: list[Category] = await uow.categories.get_all()
                incomes_list = []
                expenses_list = []
                investments_list = []
                savings_list = []
                for category in categories:
                    if category.type == "INCOME":
                        incomes_list.append(category.name)
                    if category.type == "EXPENSE":
                        expenses_list.append(category.name)
                    if category.type == "INVESTMENT":
                        investments_list.append(category.name)
                    if category.type == "SAVING":
                        savings_list.append(category.name)

                result = {
                    "categories": {
                        "incomes": incomes_list,
                        "expenses": expenses_list,
                        "investments": investments_list,
                        "savings": savings_list,
                    }
                }
                return result

        except Exception:
            raise

    @staticmethod
    async def delete_category(
        uow: UnitOfWork,
        cat_id: int,
    ) -> dict[str, int] | None:
        try:
            async with uow:
                deleted_cat_id = await uow.categories.delete_one(_id=cat_id)
                return {"deleted_id": deleted_cat_id}
        except Exception:
            raise
