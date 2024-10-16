import pytest
from httpx import AsyncClient


@pytest.mark.asyncio(loop_scope="session")
async def test_periods_get_all_router(aclient: AsyncClient, user_token: str):
    response = await aclient.get(
        "/categories/all",
        headers={"Authorization": user_token},
    )

    assert response.status_code == 200


@pytest.mark.asyncio(loop_scope="session")
async def test_periods_add_router(aclient: AsyncClient, user_token: str):
    new_period = {
        "name": "October",
        "start": "2024-01-01",
        "end": "2024-01-31",
    }
    response = await aclient.post(
        "/periods/add",
        json=new_period,
        headers={"Authorization": user_token},
    )
    data = response.json()

    assert response.status_code == 201
    assert data.get("message") == "success"
    assert data.get("data").get("new_period_id") == 1
