import pytest
from httpx import AsyncClient


@pytest.mark.asyncio(loop_scope="session")
async def test_categories_get_all_router(aclient: AsyncClient, user_token: str):
    response = await aclient.get(
        "/categories/all",
        headers={"Authorization": user_token},
    )

    assert response.status_code == 200


@pytest.mark.asyncio(loop_scope="session")
async def test_category_add_router(aclient: AsyncClient, admin_token):
    new_category = {
        "name": "test-category",
        "type": "EXPENSE",
    }
    response = await aclient.post(
        "/categories/add",
        json=new_category,
        headers={"Authorization": admin_token},
    )
    data = response.json()

    assert response.status_code == 201
    assert data.get("message") == "success"
    assert data.get("data").get("new_category_id") == 1
