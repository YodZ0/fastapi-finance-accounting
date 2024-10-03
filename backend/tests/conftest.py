import pytest

from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport

from src.actions.create_superuser import create_superuser
from src.main import main_app
from src.core.models import Base
from src.core.models.database import DataBaseHelper, get_db_helper


test_db_helper = DataBaseHelper(
    url="postgresql+asyncpg://postgres:123@localhost:5432/tests"
)


async def create_tables():
    async with test_db_helper.engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)


async def delete_tables():
    async with test_db_helper.engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)


async def override_get_db_helper() -> DataBaseHelper:
    return test_db_helper


@pytest.fixture(autouse=True, scope="session")
async def setup_override_dependencies():
    main_app.dependency_overrides[get_db_helper] = override_get_db_helper
    yield
    main_app.dependency_overrides.clear()


@pytest.fixture(autouse=True, scope="session")
async def prepare_db():
    await create_tables()
    yield
    await delete_tables()


@pytest.fixture(scope="session")
async def aclient() -> AsyncGenerator["AsyncClient", None]:
    async with AsyncClient(
        transport=ASGITransport(app=main_app),
        base_url="http://test/api/v1",
    ) as ac:
        yield ac


@pytest.fixture(scope="session")
async def user_token(aclient: AsyncClient):
    new_user = {
        "email": "antoion-banderas@tests.com",
        "password": "test123",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "username": "Antonio Banderas",
    }

    register_response = await aclient.post("/auth/register", json=new_user)
    assert register_response.status_code == 201

    login_data = {
        "username": new_user["email"],
        "password": new_user["password"],
        "grant_type": "password",
    }

    login_response = await aclient.post(
        "/auth/login",
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert login_response.status_code == 200

    token = login_response.json().get("access_token")
    assert token is not None

    return f"Bearer {token}"


@pytest.fixture(scope="session")
async def admin_token(aclient: AsyncClient):
    new_admin = {
        "email": "admin@tests.com",
        "password": "admin",
        "is_active": True,
        "is_superuser": True,
        "is_verified": True,
        "username": "Admin",
    }

    admin_user = await create_superuser(test_db_helper, **new_admin)
    assert admin_user.is_superuser is True

    login_data = {
        "username": new_admin["email"],
        "password": new_admin["password"],
        "grant_type": "password",
    }

    login_response = await aclient.post(
        "/auth/login",
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert login_response.status_code == 200

    token = login_response.json().get("access_token")
    assert token is not None

    return f"Bearer {token}"
