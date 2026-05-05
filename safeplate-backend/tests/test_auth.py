import pytest
from fastapi.testclient import TestClient
import main

client = TestClient(main.app)


class TestAuthAPI:

    def test_register_new_user_success(self):
        response = client.post("/auth/register", json={
            "email": "brandnew@example.com",
            "password": "newpass123"
        })
        assert response.status_code == 200
        assert response.json()["email"] == "brandnew@example.com"

    def test_login_valid_credentials(self, test_user):
        response = client.post("/auth/token", data={
            "username": test_user.email,
            "password": "secret123"
        })
        assert response.status_code == 200
        assert "access_token" in response.json()

    def test_login_wrong_password(self, test_user):
        response = client.post("/auth/token", data={
            "username": test_user.email,
            "password": "wrongpassword"
        })
        assert response.status_code == 401

    def test_get_current_user(self, user_token):
        response = client.get(
            "/auth/me",
            headers={"Authorization": f"Bearer {user_token}"}
        )
        assert response.status_code == 200
        assert response.json()["email"] == "test@example.com"