from sqlalchemy.exc import IntegrityError

from src.core.schemas.category import CategoryCreate
from src.utils.unit_of_work import UnitOfWork


class CategoryService:
    @staticmethod
    async def create_category(
        uow: UnitOfWork,
        new_category: CategoryCreate,
    ) -> int | None:
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
    ) -> dict[str, dict[str, list[str]]]:
        # {
        #     "categories": {
        #         "incomes": ["Cat1", "Cat2"],
        #         "expenses": ["Cat1", "Cat2"],
        #         "investments": ["Cat1", "Cat2"],
        #         "savings": ["Cat1", "Cat2"],
        #     }
        # }
        try:
            async with uow:
                categories = await uow.categories.get_all()
                return {}
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
