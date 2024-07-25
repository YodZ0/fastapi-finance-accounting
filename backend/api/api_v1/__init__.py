from fastapi import APIRouter

from core.config import settings
from .operations import router as operations_router

# Main API V1 router
router = APIRouter(
    prefix=settings.api.v1.prefix,
)

# Add api_v1 routers here
router.include_router(
    operations_router,
    prefix=settings.api.v1.operations,
    tags=['Operations'],
)
