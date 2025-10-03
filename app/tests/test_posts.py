import pytest

@pytest.mark.asyncio
class TestPosts:
    def test_create_post(self, client):
        # First create a user
        user_data = {
            "name": "Post Author",
            "email": "author@example.com"
        }
        user_response = client.post("/users/", json=user_data)
        author_id = user_response.json()["id"]
        
        # Create a post
        post_data = {
            "title": "Test Post",
            "content": "This is a test post content",
            "author_id": author_id
        }
        
        response = client.post("/posts/", json=post_data)
        assert response.status_code == 201
        
        data = response.json()
        assert data["title"] == post_data["title"]
        assert data["author_id"] == author_id

    def test_create_post_invalid_author(self, client):
        post_data = {
            "title": "Test Post",
            "content": "Content",
            "author_id": 999  # Non-existent user
        }
        
        response = client.post("/posts/", json=post_data)
        assert response.status_code == 400
        assert "does not exist" in response.json()["detail"]

    def test_get_posts(self, client):
        # Create a user and some posts
        user_data = {
            "name": "Posts Author",
            "email": "postsauthor@example.com"
        }
        user_response = client.post("/users/", json=user_data)
        author_id = user_response.json()["id"]
        
        for i in range(3):
            post_data = {
                "title": f"Post {i}",
                "content": f"Content {i}",
                "author_id": author_id
            }
            client.post("/posts/", json=post_data)
        
        response = client.get("/posts/")
        assert response.status_code == 200
        
        posts = response.json()
        assert len(posts) >= 3
        assert all("author" in post for post in posts)

    def test_get_user_posts(self, client):
        # Create a user
        user_data = {
            "name": "User Posts",
            "email": "userposts@example.com"
        }
        user_response = client.post("/users/", json=user_data)
        author_id = user_response.json()["id"]
        
        # Create posts for this user
        for i in range(2):
            post_data = {
                "title": f"User Post {i}",
                "content": f"User Content {i}",
                "author_id": author_id
            }
            client.post("/posts/", json=post_data)
        
        response = client.get(f"/posts/user/{author_id}")
        assert response.status_code == 200
        
        posts = response.json()
        assert len(posts) == 2
        assert all(post["author_id"] == author_id for post in posts)

    def test_update_post(self, client):
        # Create a user and post
        user_data = {
            "name": "Update Author",
            "email": "updateauthor@example.com"
        }
        user_response = client.post("/users/", json=user_data)
        author_id = user_response.json()["id"]
        
        post_data = {
            "title": "Original Title",
            "content": "Original content",
            "author_id": author_id
        }
        post_response = client.post("/posts/", json=post_data)
        post_id = post_response.json()["id"]
        
        # Update the post
        update_data = {
            "title": "Updated Title",
            "content": "Updated content"
        }
        response = client.put(f"/posts/{post_id}", json=update_data)
        assert response.status_code == 200
        
        updated_post = response.json()
        assert updated_post["title"] == "Updated Title"
        assert updated_post["content"] == "Updated content"

    def test_delete_post(self, client):
        # Create a user and post
        user_data = {
            "name": "Delete Author",
            "email": "deleteauthor@example.com"
        }
        user_response = client.post("/users/", json=user_data)
        author_id = user_response.json()["id"]
        
        post_data = {
            "title": "Delete Me",
            "content": "Content to delete",
            "author_id": author_id
        }
        post_response = client.post("/posts/", json=post_data)
        post_id = post_response.json()["id"]
        
        # Delete the post
        response = client.delete(f"/posts/{post_id}")
        assert response.status_code == 200
        assert response.json()["message"] == "Post deleted successfully"
        
        # Verify post is deleted
        get_response = client.get(f"/posts/{post_id}")
        assert get_response.status_code == 404