from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

from src.core.config import settings

from src.api.api_v1.auth import router as auth_router
from src.api.api_v1.users import router as users_router
from src.api.api_v1.category import router as category_router
from src.api.api_v1.period import router as period_router
from src.api.api_v1.operation import router as operation_router

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
    period_router,
    prefix=settings.api.v1.periods,
    tags=["Periods"],
)
router.include_router(
    operation_router,
    prefix=settings.api.v1.operations,
    tags=["Operations"],
)
