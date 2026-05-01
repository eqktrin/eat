import pytest
from fastapi.testclient import TestClient
from main import app
import os

os.environ["WEATHER_API_KEY"] = "test_key"

client = TestClient(app)

class TestMainApp:
    
    def test_root_endpoint(self):
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "SafePlate FastAPI backend is running" in data["message"]
    
    def test_routes_endpoint(self):
        response = client.get("/routes")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        
        for route in data:
            assert "path" in route
            assert "methods" in route
            assert isinstance(route["methods"], list)
    
    def test_cors_headers(self):
        response = client.options("/", headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "GET"
        })
        assert "access-control-allow-origin" in response.headers
        assert response.headers["access-control-allow-origin"] in [
            "http://localhost:3000",
            "http://127.0.0.1:3000"
        ]
    
    def test_static_files_mounted(self):
        response = client.get("/uploads/")
        assert response.status_code in [200, 404]
    
    def test_all_routers_are_accessible(self):
        endpoints_to_check = [
            ("/auth/me", 401),
            ("/menu/", 401),
            ("/profile/me", 401),
            ("/favorites/my", 401),
            ("/allergens/", 200),
            ("/ai/test", 200),
            ("/robots.txt", 200),
            ("/sitemap.xml", 200),
        ]
        
        for path, expected_status in endpoints_to_check:
            response = client.get(path)
            assert response.status_code == expected_status, f"Failed for {path}"


class TestCORSConfiguration:
    
    def test_cors_allows_credentials(self):
        response = client.options("/", headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "GET",
            "Access-Control-Request-Headers": "Authorization"
        })
        assert response.headers.get("access-control-allow-credentials") == "true"
    
    def test_cors_allows_all_methods(self):
        response = client.options("/", headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "POST"
        })
        assert "access-control-allow-methods" in response.headers
        methods = response.headers["access-control-allow-methods"]
        assert "GET" in methods
        assert "POST" in methods
        assert "PUT" in methods
        assert "DELETE" in methods


class TestStaticFiles:
    
    def test_uploads_directory_created(self):
        import os
        assert os.path.exists("uploads"), "Папка uploads не создана"
        assert os.path.isdir("uploads"), "uploads не является папкой"
    
    def test_uploads_mounted_correctly(self):
        response = client.get("/routes")
        routes = response.json()
        uploads_routes = [r for r in routes if r["path"].startswith("/uploads")]
        assert len(uploads_routes) > 0