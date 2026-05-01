import pytest
import pytest_asyncio
import os
from httpx import AsyncClient, ASGITransport

TEST_DB = "/tmp/test_tasks.db"
os.environ["DATABASE_URL"] = TEST_DB

from app.main import app
from app.database import create_tables


@pytest_asyncio.fixture
async def client():
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

    await create_tables()

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        yield ac

    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
        
async def test_health_check(client):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


async def test_create_task(client):
    response = await client.post("/tasks/", json={
        "title": "Buy groceries",
        "description": "Milk, eggs, bread",
    })
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Buy groceries"
    assert data["status"] == "pending"
    assert data["id"] is not None
    assert data["completed_at"] is None