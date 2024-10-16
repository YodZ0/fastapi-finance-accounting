from sqlalchemy.exc import IntegrityError

from src.core.models.user import User
from src.core.schemas.period import PeriodCreate
from src.utils.unit_of_work import UnitOfWork


class PeriodService:
    @staticmethod
    async def create_period(
        uow: UnitOfWork,
        new_period: PeriodCreate,
        user: User,
    ):
        period_dict = new_period.model_dump()
        user_id = user.id
        period_dict["user_id"] = user_id
        try:
            async with uow:
                new_period_id = await uow.periods.add_one(data=period_dict)
                return {"new_period_id": new_period_id}
        except IntegrityError:
            raise
        except Exception:
            raise

    @staticmethod
    async def get_all_user_periods(
        uow: UnitOfWork,
        user: User,
    ):
        user_id = user.id
        try:
            async with uow:
                periods = await uow.periods.get_all_filtered(user_id=user_id)
                return {"periods": periods}
        except IntegrityError:
            raise
        except Exception:
            raise
