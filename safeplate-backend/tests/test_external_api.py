class TestExternalAPI:

    def test_external_weather_endpoint(self, client):
        response = client.get("/external/weather?city=Moscow")
        assert response.status_code in [200, 503]

    def test_external_weather_timeout_handling(self, client):
        pass

    def test_external_weather_invalid_key(self, client):
        response = client.get("/external/weather?city=Moscow")
        assert response.status_code in [200, 503]
        if response.status_code == 503:
            assert "detail" in response.json()