
from fastapi import HTTPException

from Intuit.UpWork.src.database.postgres import get_postgres_conn, release_postgres_conn
from Intuit.UpWork.src.models.job import Job


async def create_job(job: Job):
    conn = get_postgres_conn()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO jobs (title, description, budget, currency, user_id) VALUES (%s, %s, %s, %s, %s) RETURNING id",
            (job.title, job.description, job.budget, job.currency, job.user_id)
        )
        job_id = cursor.fetchone()[0]
        conn.commit()
        return {"id": job_id, **job.dict()}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        release_postgres_conn(conn)

async def get_job(job_id: int):
    conn = get_postgres_conn()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, title, description, budget, currency, user_id FROM jobs WHERE id = %s", (job_id,))
        job = cursor.fetchone()
        if job:
            return {"id": job[0], "title": job[1], "description": job[2], "budget": job[3], "currency": job[4], "user_id": job[5]}
        else:
            raise HTTPException(status_code=404, detail="Job not found")
    finally:
        cursor.close()
        release_postgres_conn(conn)
