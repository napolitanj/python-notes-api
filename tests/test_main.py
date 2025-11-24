import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_health():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/notes")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_create_note():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        payload = {"text": "Test note", "category": "general"}
        response = await ac.post("/notes", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["text"] == "Test note"
    assert data["category"] == "general"
    assert "id" in data
