from sqlalchemy.exc import IntegrityError

from .schemas import RoleCreate, Role
from utils.unit_of_work import UnitOfWork


class RoleService:
    @staticmethod
    async def create_role(
            uow: UnitOfWork,
            new_role: RoleCreate,
    ):
        role_dict = new_role.model_dump()
        try:
            async with uow:
                role_id = await uow.roles.add_one(data=role_dict)
                await uow.commit()
                return role_id
        except IntegrityError:
            raise

    @staticmethod
    async def get_all_roles(
            uow: UnitOfWork,
    ) -> list[Role]:
        try:
            async with uow:
                roles = await uow.roles.get_all()
                return roles
        except Exception:
            raise

    @staticmethod
    async def delete_role(
            uow: UnitOfWork,
            role_id: int,
    ) -> int | None:
        async with uow:
            deleted_role = await uow.roles.delete_one(_id=role_id)
            await uow.commit()
            return deleted_role
