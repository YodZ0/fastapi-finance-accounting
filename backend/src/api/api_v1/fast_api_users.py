import uuid

from fastapi_users import FastAPIUsers

from src.core.models import User
from src.api.dependencies.auth.user_manager import get_user_manager
from src.api.dependencies.auth.backend import authentication_backend

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [authentication_backend],
)

current_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
