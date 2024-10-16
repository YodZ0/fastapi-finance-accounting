import pytest
from httpx import AsyncClient


@pytest.fixture(scope="session")
async def create_category(aclient: AsyncClient, admin_token: str) -> int:
    new_category = {
        "name": "operations-expense-category",
        "type": "EXPENSE",
    }
    response = await aclient.post(
        "/categories/add",
        json=new_category,
        headers={"Authorization": admin_token},
    )
    data = response.json()
    cat_id = data.get("data").get("new_category_id")
    return cat_id


@pytest.fixture(scope="session")
async def create_period(aclient: AsyncClient, user_token: str) -> int:
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
    period_id = data.get("data").get("new_period_id")
    return period_id


@pytest.mark.asyncio(loop_scope="session")
async def test_operations_add_router(
    aclient: AsyncClient,
    user_token: str,
    create_category: int,
    create_period: int,
):
    new_operation = {
        "name": "test",
        "amount": 123.20,
        "currency": "KZT",
        "date": "2024-10-16",
        "category_id": create_category,
        "period_id": create_period,
    }
    response = await aclient.post(
        "/operations/add",
        json=new_operation,
        headers={"Authorization": user_token},
    )
    data = response.json()

    assert response.status_code == 201
    assert data.get("message") == "success"
    assert data.get("data").get("new_operation_id") == 1


@pytest.mark.asyncio(loop_scope="session")
async def test_operations_get_all_router(
    aclient: AsyncClient,
    user_token: str,
    create_period: int,
    create_category: int,
):
    response = await aclient.get(
        "/operations/all",
        headers={"Authorization": user_token},
    )
    res = response.json()
    data = res.get("data")
    operations = data.get("operations")

    assert response.status_code == 200
    assert data is not None
    assert operations is not None
    assert len(operations) == 1

    first = operations[0]
    assert first.get("name") == "test"
    assert first.get("amount") == 123.20
    assert first.get("currency") == "KZT"
    assert first.get("date") == "2024-10-16"
    assert first.get("period_id") == create_period
    assert first.get("category_id") == create_category


@pytest.mark.asyncio(loop_scope="session")
async def test_operations_delete_router(aclient: AsyncClient, user_token: str):
    operation_id = 1

    response = await aclient.delete(
        f"/periods/delete/{operation_id}",
        headers={"Authorization": user_token},
    )
    data = response.json()

    assert response.status_code == 200
    assert data.get("message") == "success"
    assert data.get("data").get("deleted_id") == 1

    operation_id = 2

    response = await aclient.delete(
        f"/operations/delete/{operation_id}",
        headers={"Authorization": user_token},
    )

    assert response.status_code == 404
