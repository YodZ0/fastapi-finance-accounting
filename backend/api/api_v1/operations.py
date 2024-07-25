from fastapi import APIRouter

router = APIRouter()


@router.get('')
async def get_operations_list():
    pass
