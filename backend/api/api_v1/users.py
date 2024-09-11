from fastapi import APIRouter

from .fast_api_users import fastapi_users

from core.schemas.user import UserRead, UserUpdate

router = APIRouter()

# /me
# /{id}
# /delete/{id}
router.include_router(
    router=fastapi_users.get_users_router(
        UserRead,
        UserUpdate,
    ),
)
