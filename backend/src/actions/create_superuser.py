import contextlib
from typing import Annotated, TYPE_CHECKING

from fastapi import Depends

from src.core.models import User
from src.core.auth.user_manager import UserManager
from src.core.models.database import get_db_helper
from src.core.schemas.user import UserCreate

from src.api.dependencies.auth.user_manager import get_user_manager
from src.api.dependencies.auth.users import get_users_db

if TYPE_CHECKING:
    from src.core.models.database import DataBaseHelper

get_users_db_context = contextlib.asynccontextmanager(get_users_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)

default_username = "admin"
default_email = "admin@admin.com"
default_password = "admin"
default_is_active = True
default_is_superuser = True
default_is_verified = True


async def create_user(
    user_manager: UserManager,
    user_create: UserCreate,
) -> User:
    user = await user_manager.create(
        user_create=user_create,
        safe=False,
    )
    return user


async def create_superuser(
    db_helper: Annotated["DataBaseHelper", Depends(get_db_helper)],
    username: str = default_username,
    email: str = default_email,
    password: str = default_password,
    is_active: bool = default_is_active,
    is_superuser: bool = default_is_superuser,
    is_verified: bool = default_is_verified,
):
    user_create = UserCreate(
        username=username,
        email=email,
        password=password,
        is_active=is_active,
        is_superuser=is_superuser,
        is_verified=is_verified,
    )
    async with get_users_db_context(db_helper) as user_db:
        async with get_user_manager_context(user_db) as user_manager:
            return await create_user(
                user_manager=user_manager,
                user_create=user_create,
            )
