import pytest
from fastapi.testclient import TestClient
import main

client = TestClient(main.app)


class TestMainApp:

    def test_root_endpoint(self):
        response = client.get("/")
        assert response.status_code == 200

    def test_cors_headers(self):
        response = client.options("/", headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "GET"
        })
        assert "access-control-allow-origin" in response.headers

    def test_all_routers_are_accessible(self, user_token):
        endpoints_to_check = [
            ("/auth/me", 401),
            ("/menu/", 200),
            ("/profile/me", 401),
            ("/robots.txt", 200),
            ("/sitemap.xml", 200),
        ]

        for path, expected in endpoints_to_check:
            if path == "/menu/":
                response = client.get(path, headers={"Authorization": f"Bearer {user_token}"})
            else:
                response = client.get(path)
            assert response.status_code in [expected, 200]