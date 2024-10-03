import uuid
from typing import Optional, TYPE_CHECKING

from fastapi_users import BaseUserManager, UUIDIDMixin

from src.core.config import settings
from src.core.models import User
from src.loggers import get_logger

if TYPE_CHECKING:
    from fastapi import Request

logger = get_logger(__name__)


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = settings.access_token.reset_password_token_secret
    verification_token_secret = settings.access_token.verification_token_secret

    async def on_after_register(
        self,
        user: User,
        request: Optional["Request"] = None,
    ):
        logger.success(
            "User {user_email} ({user_id}) has registered.",
            user_email=user.email,
            user_id=user.id,
        )

    async def on_after_forgot_password(
        self,
        user: User,
        token: str,
        request: Optional["Request"] = None,
    ):
        logger.info(
            "User {user_email} ({user_id}) has forgot their password. Reset token: {token}",
            user_email=user.email,
            user_id=user.id,
            token=token,
        )

    async def on_after_request_verify(
        self,
        user: User,
        token: str,
        request: Optional["Request"] = None,
    ):
        logger.success(
            "Verification requested for user {user_email} ({user_id}). Verification token: {token}.",
            user_email=user.email,
            user_id=user.id,
            token=token,
        )
