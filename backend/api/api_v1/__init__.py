from fastapi import APIRouter

from core.config import settings

from modules.categories.routers import router as category_router
from modules.roles.routers import router as role_router

# Main API V1 router
router = APIRouter(
    prefix=settings.api.v1.prefix,
)

# Add api_v1 routers here
router.include_router(
    category_router,
    prefix=settings.api.v1.categories,
    tags=['Categories'],
)
router.include_router(
    role_router,
    prefix=settings.api.v1.roles,
    tags=['Roles'],
)
