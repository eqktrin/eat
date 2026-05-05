import pytest


class TestWeatherAPI:

    def test_weather_endpoint_success(self, client):
        response = client.get("/weather/?city=Moscow")
        assert response.status_code == 200
        data = response.json()

        assert "city" in data
        assert isinstance(data["city"], str)

    def test_weather_endpoint_default_city(self, client):
        response = client.get("/weather/")
        assert response.status_code == 200
        # Город может быть на русском или английском
        city = response.json().get("city")
        assert city in ["Москва", "Moscow"]
        
    def test_weather_endpoint_custom_city(self, client):
        response = client.get("/weather/?city=Saint%20Petersburg")
        assert response.status_code == 200

    def test_weather_cities_endpoint(self, client):
        response = client.get("/weather/cities")
        assert response.status_code == 200
        data = response.json()

        assert "cities" in data
        assert isinstance(data["cities"], list)

    def test_weather_endpoint_handles_nonexistent_city(self, client):
        response = client.get("/weather/?city=NonexistentCity12345")
        assert response.status_code in [200, 503]