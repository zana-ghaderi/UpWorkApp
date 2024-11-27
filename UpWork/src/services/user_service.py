import json

from Intuit.MyBook.src.database.postgres import get_postgres_conn, get_postgres_cursor
from Intuit.MyBook.src.models.user import User
from fastapi import HTTPException
import bcrypt

from Intuit.UpWork.src.database.cache import get_redis_client

redis_cache = get_redis_client()


async def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


async def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


async def create_user(user: User):
    conn = get_postgres_conn()
    cursor = get_postgres_cursor(conn)
    try:
        hashed_password = await hash_password(user.password)
        cursor.execute(
            "INSERT INTO users (email, name, role, hashed_password) VALUES (%s, %s, %s, %s) RETURNING id",
            (user.email, user.name, user.role, hashed_password)
        )
        user_id = cursor.fetchone()['id']
        conn.commit()
        return {"id": user_id, **user.dict()}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()


async def get_user(user_id: int):
    try:
        cache_data = redis_cache.get(user_id)
        if cache_data:
            cache_data = json.loads(cache_data)
            if cache_data:
                return cache_data
    finally:
        conn = get_postgres_conn()
        cursor = get_postgres_cursor(conn)
        try:
            cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
            user = cursor.fetchone()
            if user:
                redis_cache.set(user_id, json.dumps(user))
                return user
            else:
                raise HTTPException(status_code=404, detail="User not found")
        finally:
            cursor.close()
            conn.close()
