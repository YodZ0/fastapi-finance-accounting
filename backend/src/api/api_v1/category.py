from fastapi import APIRouter, HTTPException, Depends, status

from sqlalchemy.exc import IntegrityError

from src.api.api_v1.dependencies import UOWDep
from .fast_api_users import current_user, current_superuser

from src.services.category import CategoryService
from src.core.schemas.category import CategoryCreate

router = APIRouter()


@router.post(
    "/add",
    status_code=status.HTTP_201_CREATED,
    description="Create new category.",
    dependencies=[Depends(current_superuser)],
)
async def create_category(
    uow: UOWDep,
    new_category: CategoryCreate,
):
    try:
        new_cat_id = await CategoryService().create_category(uow, new_category)
        return {"message": "success", "data": new_cat_id}

    except IntegrityError:
        raise HTTPException(
            status_code=400, detail="Category name must be unique. Try another name."
        )
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error.")


@router.get(
    "/all",
    status_code=status.HTTP_200_OK,
    description="Get all categories, grouped by their types: INCOMES, EXPENSES, INVESTMENTS, SAVINGS.",
    dependencies=[Depends(current_user)],
)
async def get_all_categories(
    uow: UOWDep,
):
    try:
        categories_dict = await CategoryService().get_all_categories(uow)
        return {"message": "success", "data": categories_dict}
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error.")


@router.delete(
    "/delete/{id}",
    status_code=status.HTTP_200_OK,
    description="Delete the category.",
    dependencies=[Depends(current_superuser)],
)
async def delete_category(
    uow: UOWDep,
    cat_id: int,
):
    deleted_id = await CategoryService().delete_category(uow, cat_id)
    if deleted_id:
        return {"deleted_id": str(deleted_id), "message": "success", "status": "200"}
    else:
        return {"message": "Object not found", "status_code": "404"}
