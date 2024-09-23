import uuid
from typing import Optional, TYPE_CHECKING

from fastapi_users import BaseUserManager, UUIDIDMixin

from src.core.config import settings
from src.core.models import User

if TYPE_CHECKING:
    from fastapi import Request


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = settings.access_token.reset_password_token_secret
    verification_token_secret = settings.access_token.verification_token_secret

    async def on_after_register(
        self,
        user: User,
        request: Optional["Request"] = None,
    ):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self,
        user: User,
        token: str,
        request: Optional["Request"] = None,
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self,
        user: User,
        token: str,
        request: Optional["Request"] = None,
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")
