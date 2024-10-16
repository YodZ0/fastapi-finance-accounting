import uuid
import datetime

from fastapi_users import schemas
from pydantic import EmailStr


class UserRead(schemas.BaseUser[uuid.UUID]):
    id: uuid.UUID
    email: EmailStr
    created_at: datetime.date

    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False


class UserCreate(schemas.BaseUserCreate):
    created_at: datetime.date = datetime.date.today()


class UserUpdate(schemas.BaseUserUpdate):
    pass
