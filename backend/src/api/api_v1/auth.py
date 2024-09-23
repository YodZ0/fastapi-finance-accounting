from fastapi import APIRouter

from .fast_api_users import fastapi_users
from src.api.dependencies.auth.backend import authentication_backend

from src.core.schemas.user import UserRead, UserCreate

router = APIRouter()

# /login
# /logout
router.include_router(
    router=fastapi_users.get_auth_router(
        authentication_backend,
    ),
)

# /register
router.include_router(
    router=fastapi_users.get_register_router(
        UserRead,
        UserCreate,
    ),
)

# /request-verify-token
# /verify
router.include_router(
    router=fastapi_users.get_verify_router(UserRead),
)

# /forgot-password
# /reset-password
router.include_router(
    router=fastapi_users.get_reset_password_router(),
)
