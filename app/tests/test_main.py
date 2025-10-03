import pytest

class TestMainEndpoints:
    def test_root_endpoint(self, client):
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "timestamp" in data

    def test_stats_endpoint(self, client):
        response = client.get("/stats")
        assert response.status_code == 200
        data = response.json()
        assert "total_users" in data
        assert "total_posts" in data
        assert "avg_name_length" in data

    def test_docs_endpoint(self, client):
        response = client.get("/docs")
        assert response.status_code == 200

    def test_redoc_endpoint(self, client):
        response = client.get("/redoc")
        assert response.status_code == 200