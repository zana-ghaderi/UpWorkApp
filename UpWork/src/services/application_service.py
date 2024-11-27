
from fastapi import HTTPException

from Intuit.UpWork.src.database.postgres import get_postgres_conn, release_postgres_conn
from Intuit.UpWork.src.models.application import Application


async def create_application(application: Application):
    conn = get_postgres_conn()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO applications (job_id, user_id, proposal) VALUES (%s, %s, %s) RETURNING id",
            (application.job_id, application.user_id, application.proposal)
        )
        app_id = cursor.fetchone()[0]
        conn.commit()
        return {"id": app_id, **application.dict()}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        release_postgres_conn(conn)

async def get_application(app_id: int):
    conn = get_postgres_conn()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, job_id, user_id, proposal FROM applications WHERE id = %s", (app_id,))
        application = cursor.fetchone()
        if application:
            return {"id": application[0], "job_id": application[1], "user_id": application[2], "proposal": application[3]}
        else:
            raise HTTPException(status_code=404, detail="Application not found")
    finally:
        cursor.close()
        release_postgres_conn(conn)
