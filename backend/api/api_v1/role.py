from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from sqlalchemy.exc import IntegrityError

from api.api_v1.dependencies import UOWDep
from .fast_api_users import current_superuser

from services.role import RoleService
from core.schemas.role import Role, RoleCreate

router = APIRouter()


@router.post("/add", dependencies=[Depends(current_superuser)])
async def create_role(
    uow: UOWDep,
    new_role: RoleCreate,
):
    try:
        new_role_id = await RoleService().create_role(uow, new_role)
        return JSONResponse(
            status_code=201,
            content={"message": "Role created successfully", "id": new_role_id},
        )
    except IntegrityError:
        raise HTTPException(
            status_code=400, detail="Role name must be unique. Try another name."
        )
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error.")


@router.get("/all", dependencies=[Depends(current_superuser)])
async def get_all_roles(
    uow: UOWDep,
) -> list[Role]:
    try:
        roles = await RoleService().get_all_roles(uow)
        return roles
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error.")


@router.delete("/delete/{id}", dependencies=[Depends(current_superuser)])
async def delete_role(
    uow: UOWDep,
    role_id: int,
) -> dict:
    deleted_id = await RoleService().delete_role(uow, role_id)
    if deleted_id:
        return {"deleted_id": str(deleted_id), "message": "success", "status": "200"}
    else:
        return {"message": "Object not found", "status_code": "404"}
