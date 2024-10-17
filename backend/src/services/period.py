from sqlalchemy.exc import IntegrityError

from src.core.models.user import User
from src.core.schemas.period import PeriodCreate, Period
from src.utils.unit_of_work import UnitOfWork


class PeriodService:
    @staticmethod
    async def create_period(
        uow: UnitOfWork,
        new_period: PeriodCreate,
        user: User,
    ) -> dict[str, int]:
        period_dict = new_period.model_dump()
        period_dict["user_id"] = user.id
        try:
            async with uow:
                new_period_id = await uow.periods.add_one(**period_dict)
                return {"new_period_id": new_period_id}
        except IntegrityError:
            raise
        except Exception:
            raise

    @staticmethod
    async def get_all_user_periods(
        uow: UnitOfWork,
        user: User,
    ) -> dict[str, list[Period]]:
        try:
            async with uow:
                periods: list = await uow.periods.get_filtered(user_id=user.id)
                result = [Period.model_validate(period) for period in periods]
                return {"periods": result}
        except IntegrityError:
            raise
        except Exception:
            raise

    @staticmethod
    async def delete_period(
        uow: UnitOfWork,
        period_id: int,
        user: User,
    ) -> dict[str, int] | None:
        try:
            async with uow:
                period = await uow.periods.get_one_by_pk(pk=period_id)
                if period:
                    period = Period.model_validate(period)
                    if period.user_id == user.id:
                        deleted_period_id = await uow.periods.delete_one(pk=period_id)
                        return {"deleted_id": deleted_period_id}
                else:
                    return None
        except Exception:
            raise
