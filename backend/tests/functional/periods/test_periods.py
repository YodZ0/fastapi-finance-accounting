import pytest
from httpx import AsyncClient


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


@pytest.mark.asyncio(loop_scope="session")
async def test_periods_get_all_router(aclient: AsyncClient, user_token: str):
    response = await aclient.get(
        "/periods/all",
        headers={"Authorization": user_token},
    )
    res = response.json()
    data = res.get("data")
    periods = data.get("periods")
    first = periods[0]

    assert response.status_code == 200
    assert data is not None
    assert periods is not None
    assert len(periods) == 1
    assert first.get("name") == "October"
    assert first.get("start") == "2024-01-01"
    assert first.get("end") == "2024-01-31"
