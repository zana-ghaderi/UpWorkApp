from fastapi import APIRouter

from Intuit.UpWork.src.models.application import Application
from Intuit.UpWork.src.services.application_service import create_application, get_application

router = APIRouter()

@router.post("/applications/")
async def add_application(application: Application):
    return await create_application(application)

@router.get("/applications/{app_id}")
async def read_application(app_id: int):
    return await get_application(app_id)
