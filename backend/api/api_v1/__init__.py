from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

from core.config import settings

from api.api_v1.auth import router as auth_router
from api.api_v1.users import router as users_router
from api.api_v1.category import router as category_router
from api.api_v1.role import router as role_router

http_bearer = HTTPBearer(auto_error=False)

# Main API V1 router
router = APIRouter(
    prefix=settings.api.v1.prefix,
    dependencies=[
        Depends(http_bearer),
    ],
)

# Add api_v1 routers here
router.include_router(
    auth_router,
    prefix=settings.api.v1.auth,
    tags=["Auth"],
)
router.include_router(
    users_router,
    prefix=settings.api.v1.users,
    tags=["Users"],
)
router.include_router(
    category_router,
    prefix=settings.api.v1.categories,
    tags=["Categories"],
)
router.include_router(
    role_router,
    prefix=settings.api.v1.roles,
    tags=["Roles"],
)
