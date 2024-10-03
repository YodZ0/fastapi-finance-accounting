import pytest
from httpx import AsyncClient


@pytest.mark.asyncio(loop_scope="session")
async def test_user_me(aclient: AsyncClient, user_token: str):
    response = await aclient.get(
        "/users/me",
        headers={"Authorization": user_token},
    )

    assert response.status_code == 200
