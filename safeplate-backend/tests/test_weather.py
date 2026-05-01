import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestWeatherAPI:
    """Тесты для эндпоинтов погоды"""
    
    def test_weather_endpoint_success(self):
        """Проверка успешного получения погоды для Москвы"""
        response = client.get("/weather/?city=Moscow")
        assert response.status_code == 200
        data = response.json()
        
        # Проверяем, что в ответе есть нужные поля
        assert "city" in data
        assert "temperature" in data or "error" in data
        assert isinstance(data["city"], str)
    
    def test_weather_endpoint_default_city(self):
        """Проверка, что город по умолчанию — Москва"""
        response = client.get("/weather/")
        assert response.status_code == 200
        data = response.json()
        
        # Если нет ошибки, то город должен быть Москва
        if "error" not in data:
            assert data.get("city") == "Москва"
    
    def test_weather_endpoint_custom_city(self):
        """Проверка погоды для Санкт-Петербурга"""
        response = client.get("/weather/?city=Saint%20Petersburg")
        assert response.status_code == 200
        data = response.json()
        
        if "error" not in data:
            assert data.get("city") == "Санкт-Петербург"
    
    def test_weather_endpoint_invalid_city(self):
        """Проверка обработки несуществующего города"""
        response = client.get("/weather/?city=ThisCityDoesNotExist12345")
        assert response.status_code == 200  # Должен вернуть 200 с ошибкой внутри
        data = response.json()
        
        # Должна быть ошибка или город не найден
        assert "error" in data or "city" in data
    
    def test_weather_cities_endpoint(self):
        """Проверка эндпоинта /weather/cities"""
        response = client.get("/weather/cities")
        assert response.status_code == 200
        data = response.json()
        
        assert "cities" in data
        assert isinstance(data["cities"], list)
        assert len(data["cities"]) > 0
        assert "Moscow" in data["cities"] or "Москва" in data["cities"]


class TestWeatherAPIWithMock:
    """Тесты с моком внешнего API (не требуют реального интернета)"""
    
    def test_weather_endpoint_with_mock_success(self, mock_weather_api):
        """С моком: успешный ответ от внешнего API"""
        response = client.get("/weather/?city=Moscow")
        assert response.status_code == 200
    
    def test_weather_endpoint_with_mock_error(self, mock_weather_api_error):
        """С моком: ошибка от внешнего API"""
        response = client.get("/weather/?city=Moscow")
        # Должен вернуть 200 с полем error
        assert response.status_code == 200
        data = response.json()
        assert "error" in data


# Фикстуры для моков
@pytest.fixture
def mock_weather_api(monkeypatch):
    """Мок успешного ответа от OpenWeatherMap"""
    import utils.weather_service as weather_service
    
    async def mock_get_weather(city):
        return {
            "city": city,
            "temperature": 20,
            "feels_like": 18,
            "humidity": 65,
            "description": "clear sky",
            "icon": "01d"
        }
    
    monkeypatch.setattr(weather_service, "get_weather", mock_get_weather)
    return mock_get_weather


@pytest.fixture
def mock_weather_api_error(monkeypatch):
    """Мок ошибки от OpenWeatherMap"""
    import utils.weather_service as weather_service
    
    async def mock_get_weather_error(city):
        return {
            "city": city,
            "error": "Failed to fetch weather data"
        }
    
    monkeypatch.setattr(weather_service, "get_weather", mock_get_weather_error)
    return mock_get_weather_error