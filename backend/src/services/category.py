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
                new_category_id = await uow.categories.add_one(**category_dict)
                return {"new_category_id": new_category_id}
        except IntegrityError:
            raise
        except Exception:
            raise

    @staticmethod
    async def get_all_categories(
        uow: UnitOfWork,
    ) -> dict[str, dict[str, list[tuple[int, str]]]]:
        try:
            async with uow:
                category_map = {
                    "INCOME": [],
                    "EXPENSE": [],
                    "INVESTMENT": [],
                    "SAVING": [],
                    "REMAINS": [],
                }
                categories: list[Category] = await uow.categories.get_all()

                for category in categories:
                    cat = Category.model_validate(category)
                    if cat.type in category_map:
                        category_map[cat.type].append((cat.id, cat.name))

                result = {
                    "categories": {
                        "incomes": category_map["INCOME"],
                        "expenses": category_map["EXPENSE"],
                        "investments": category_map["INVESTMENT"],
                        "savings": category_map["SAVING"],
                        "remains": category_map["REMAINS"],
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
                deleted_cat_id = await uow.categories.delete_one(pk=cat_id)
                return {"deleted_id": deleted_cat_id}
        except Exception:
            raise
