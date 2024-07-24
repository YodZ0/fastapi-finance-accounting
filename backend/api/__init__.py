from fastapi import APIRouter
from core.config import settings

# Main API router
router = APIRouter(
    prefix=settings.api.prefix,
    tags=settings.api.tags,
)

# Add routers here
# router.include_router()
