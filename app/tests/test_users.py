import pytest
from app.models import User

@pytest.mark.asyncio
class TestUsers:
    async def test_create_user(self, db_session):
        user = User(
            name="Test User",
            email="test@example.com",
            bio="Test bio"
        )
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)
        
        assert user.id is not None
        assert user.name == "Test User"
        assert user.email == "test@example.com"

    def test_create_user_via_api(self, client):
        user_data = {
            "name": "API User",
            "email": "api@example.com",
            "bio": "API test bio"
        }
        
        response = client.post("/users/", json=user_data)
        assert response.status_code == 201
        
        data = response.json()
        assert data["name"] == user_data["name"]
        assert data["email"] == user_data["email"]
        assert "id" in data

    def test_create_user_duplicate_email(self, client):
        user_data = {
            "name": "First User",
            "email": "duplicate@example.com"
        }
        
        # First request should succeed
        response1 = client.post("/users/", json=user_data)
        assert response1.status_code == 201
        
        # Second request should fail
        response2 = client.post("/users/", json=user_data)
        assert response2.status_code == 400
        assert "already registered" in response2.json()["detail"]

    def test_get_users(self, client):
        # Create some test users
        for i in range(3):
            user_data = {
                "name": f"User {i}",
                "email": f"user{i}@example.com"
            }
            client.post("/users/", json=user_data)
        
        response = client.get("/users/")
        assert response.status_code == 200
        
        users = response.json()
        assert len(users) >= 3
        assert all("email" in user for user in users)

    def test_get_user_by_id(self, client):
        # Create a user
        user_data = {
            "name": "Specific User",
            "email": "specific@example.com"
        }
        create_response = client.post("/users/", json=user_data)
        user_id = create_response.json()["id"]
        
        # Get the user by ID
        response = client.get(f"/users/{user_id}")
        assert response.status_code == 200
        
        user = response.json()
        assert user["id"] == user_id
        assert user["name"] == "Specific User"

    def test_get_nonexistent_user(self, client):
        response = client.get("/users/999")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

    def test_update_user(self, client):
        # Create a user
        user_data = {
            "name": "Original Name",
            "email": "original@example.com"
        }
        create_response = client.post("/users/", json=user_data)
        user_id = create_response.json()["id"]
        
        # Update the user
        update_data = {
            "name": "Updated Name",
            "email": "updated@example.com"
        }
        response = client.put(f"/users/{user_id}", json=update_data)
        assert response.status_code == 200
        
        updated_user = response.json()
        assert updated_user["name"] == "Updated Name"
        assert updated_user["email"] == "updated@example.com"

    def test_delete_user(self, client):
        # Create a user
        user_data = {
            "name": "Delete Me",
            "email": "delete@example.com"
        }
        create_response = client.post("/users/", json=user_data)
        user_id = create_response.json()["id"]
        
        # Delete the user
        response = client.delete(f"/users/{user_id}")
        assert response.status_code == 200
        assert response.json()["message"] == "User deleted successfully"
        
        # Verify user is deleted
        get_response = client.get(f"/users/{user_id}")
        assert get_response.status_code == 404