from fastapi import APIRouter

from Intuit.UpWork.src.models.user import User
from Intuit.UpWork.src.services.user_service import create_user, get_user

router = APIRouter()

@router.post("/users/")
async def add_user(user: User):
    return await create_user(user)

@router.get("/users/{user_id}")
async def read_user(user_id: int):
    return await get_user(user_id)