from fastapi import APIRouter

from Intuit.UpWork.src.models.job import Job
from Intuit.UpWork.src.services.job_service import create_job, get_job

router = APIRouter()

@router.post("/jobs/")
async def add_job(job: Job):
    return await create_job(job)

@router.get("/jobs/{job_id}")
async def read_job(job_id: int):
    return await get_job(job_id)
