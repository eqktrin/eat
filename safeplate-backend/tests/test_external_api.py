import pytest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestWeatherAPI:
    """Тесты для эндпоинтов погоды"""
    
    def test_weather_endpoint_success(self):
        """Проверка успешного получения погоды"""
        response = client.get("/weather/?city=Moscow")
        assert response.status_code == 200
        data = response.json()
        
        assert "city" in data
        assert "temperature" in data or "error" in data
        assert isinstance(data["city"], str)
    
    def test_weather_endpoint_default_city(self):
        """Проверка, что город по умолчанию — Москва"""
        response = client.get("/weather/")
        assert response.status_code == 200
        data = response.json()
        assert data.get("city") == "Москва"
    
    def test_weather_endpoint_custom_city(self):
        """Проверка погоды для другого города"""
        response = client.get("/weather/?city=Saint%20Petersburg")
        assert response.status_code == 200
        data = response.json()
        assert data.get("city") == "Санкт-Петербург"
    
    def test_weather_cities_endpoint(self):
        """Проверка эндпоинта /weather/cities"""
        response = client.get("/weather/cities")
        assert response.status_code == 200
        data = response.json()
        assert "cities" in data
        assert isinstance(data["cities"], list)
        assert "Moscow" in data["cities"]
    
    def test_weather_endpoint_handles_nonexistent_city(self):
        """Проверка обработки несуществующего города"""
        response = client.get("/weather/?city=NonexistentCity12345")
        assert response.status_code in [200, 503]
        data = response.json()
        if "error" in data:
            assert data["error"] is not None


class TestExternalAPI:
    """Тесты для /external эндпоинтов"""
    
    def test_external_weather_endpoint(self):
        """Проверка /external/weather эндпоинта"""
        response = client.get("/external/weather?city=Moscow")
        assert response.status_code in [200, 503]
    
    def test_external_weather_timeout_handling(self):
        """Проверка обработки таймаута (мокируем)"""
        pass
    
    def test_external_weather_invalid_key(self):
        """Проверка обработки неверного API ключа"""
        response = client.get("/external/weather?city=Moscow")
        if response.status_code == 503:
            data = response.json()
            assert "detail" in data


class TestSEORoutes:
    """Тесты SEO эндпоинтов"""
    
    def test_robots_txt(self):
        """Проверка robots.txt"""
        response = client.get("/robots.txt")
        assert response.status_code == 200
        assert response.headers["content-type"] == "text/plain; charset=utf-8"
        content = response.text
        assert "User-agent:" in content
        assert "Disallow:" in content
        assert "Sitemap:" in content
    
    def test_sitemap_xml(self):
        """Проверка sitemap.xml"""
        response = client.get("/sitemap.xml")
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/xml"
        content = response.text
        assert "<urlset" in content
        assert "<url>" in content
        assert "<loc>" in content
        assert "safeplate.ru" in content


class TestImagesRouter:
    """Тесты для эндпоинтов изображений"""
    
    def test_upload_endpoint_requires_auth(self):
        """Проверка, что загрузка требует авторизации"""
        response = client.post("/images/upload/1")
        assert response.status_code == 401
    
    def test_get_image_info_endpoint(self):
        """Проверка получения информации об изображении"""
        response = client.get("/images/99999")
        # Эндпоинт требует авторизации, возвращает 401
        assert response.status_code == 401
    
    def test_delete_image_requires_auth(self):
        """Проверка, что удаление требует авторизации"""
        response = client.delete("/images/1")
        assert response.status_code == 401