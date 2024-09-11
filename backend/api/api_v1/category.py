from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse

from sqlalchemy.exc import IntegrityError

from api.api_v1.dependencies import UOWDep
from .fast_api_users import current_user, current_superuser

from services.category import CategoryService
from core.schemas.category import CategoryCreate, Category

router = APIRouter()


@router.get("/generate", dependencies=[Depends(current_superuser)])
async def generate_categories(
    uow: UOWDep,
) -> dict:
    await CategoryService().generate_categories(uow)
    return {"message": "success"}


@router.post("/add", dependencies=[Depends(current_superuser)])
async def create_category(
    uow: UOWDep,
    new_category: CategoryCreate,
):
    try:
        new_cat_id = await CategoryService().create_category(uow, new_category)
        return JSONResponse(
            status_code=201,
            content={"message": "Category created successfully", "id": new_cat_id},
        )
    except IntegrityError:
        raise HTTPException(
            status_code=400, detail="Category name must be unique. Try another name."
        )
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error.")


@router.get("/all", dependencies=[Depends(current_user)])
async def get_all_categories(
    uow: UOWDep,
) -> dict[str, list[Category]]:
    try:
        categories_dict = await CategoryService().get_all_categories(uow)
        return categories_dict
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error.")


@router.delete("/delete/{id}", dependencies=[Depends(current_superuser)])
async def delete_category(
    uow: UOWDep,
    cat_id: int,
) -> dict:
    deleted_id = await CategoryService().delete_category(uow, cat_id)
    if deleted_id:
        return {"deleted_id": str(deleted_id), "message": "success", "status": "200"}
    else:
        return {"message": "Object not found", "status_code": "404"}
