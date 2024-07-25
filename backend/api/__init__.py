from fastapi import APIRouter
from core.config import settings

from .api_v1 import router as router_api_v1

# Main API router
router = APIRouter(
    prefix=settings.api.prefix,
)

# Include Api V1 router
router.include_router(router_api_v1)
