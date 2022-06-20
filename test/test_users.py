"""
test the user signup functionality
"""

from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_root():
    """Test the root path of the API"""
    res = client.get("/")
    assert res.json().get("message") == "welcome to my api!!"
    assert res.status_code == 200


def test_create_user():
    """Test that we can create a user"""
    res = client.post(
        "/users/", json={"email": "hello123@gmail.com", "password": "password123"}
    )
    print(res.json())
    assert res.status_code == 201
