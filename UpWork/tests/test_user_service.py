import pytest
from httpx import AsyncClient

from Intuit.UpWork.src.database.postgres import get_postgres_conn, release_postgres_conn
from Intuit.UpWork.src.main import app


@pytest.mark.asyncio
async def test_create_user():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/api/users/",
                                 json={"email": "test@example.com", "name": "Test User", "role": "freelancer", "password":"password"})
        assert response.status_code == 200
        assert response.json()["email"] == "test@example.com"
        assert response.json()["name"] == "Test User"
        assert response.json()["role"] == "freelancer"


@pytest.mark.asyncio
async def test_get_user():
    # Insert a user into the database for testing
    conn = get_postgres_conn()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (email, name, role, hashed_password) VALUES (%s, %s, %s) RETURNING id",
        ("fetchtest@example.com", "Fetch Test", "client", "eejw6327421#212")
    )
    user_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    release_postgres_conn(conn)

    # Test fetching the user
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(f"/api/users/{user_id}")
        assert response.status_code == 200
        assert response.json()["id"] == user_id
        assert response.json()["email"] == "fetchtest@example.com"
        assert response.json()["name"] == "Fetch Test"
        assert response.json()["role"] == "client"

    # Cleanup after the test
    conn = get_postgres_conn()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
    conn.commit()
    cursor.close()
    release_postgres_conn(conn)
