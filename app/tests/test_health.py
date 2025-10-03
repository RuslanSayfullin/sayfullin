import pytest
from app.database import health_check

@pytest.mark.asyncio
async def test_health_check(db_session):
    is_healthy = await health_check()
    assert is_healthy == True

def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "database" in data
    assert data["status"] in ["healthy", "unhealthy"]