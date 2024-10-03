import pytest
from httpx import AsyncClient


@pytest.mark.asyncio(loop_scope="session")
async def test_register_user(aclient: AsyncClient):
    new_user = {
        "email": "dummy@tests.com",
        "password": "password",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "username": "Test dummy",
    }
    response = await aclient.post("/auth/register", json=new_user)
    data = response.json()

    assert response.status_code == 201
    assert data.get("email", None) == new_user.get("email")
    assert data.get("password", None) is None


@pytest.mark.asyncio(loop_scope="session")
async def test_login_user(aclient: AsyncClient):
    user = {
        "grant_type": "password",
        "username": "dummy@tests.com",
        "password": "password",
    }
    response = await aclient.post(
        "/auth/login",
        data=user,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    data = response.json()

    assert response.status_code == 200
    assert data.get("access_token", None) is not None
