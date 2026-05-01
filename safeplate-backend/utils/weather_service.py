import httpx
import os
from cachetools import TTLCache
from dotenv import load_dotenv

load_dotenv()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"

cache = TTLCache(maxsize=100, ttl=600)

class WeatherService:
    """Сервис для работы с OpenWeatherMap API"""
    
    @staticmethod
    async def get_weather(city: str = "Moscow"):
        cache_key = f"weather_{city}"
        
        # Проверка кэша
        if cache_key in cache:
            return cache[cache_key]
        
        async with httpx.AsyncClient(timeout=5.0) as client:
            try:
                response = await client.get(
                    WEATHER_API_URL,
                    params={
                        "q": city,
                        "appid": WEATHER_API_KEY,
                        "units": "metric",
                        "lang": "ru"
                    }
                )
                response.raise_for_status()
                data = response.json()
                
                result = {
                    "city": data["name"],
                    "temperature": round(data["main"]["temp"]),
                    "feels_like": round(data["main"]["feels_like"]),
                    "humidity": data["main"]["humidity"],
                    "description": data["weather"][0]["description"],
                    "icon": data["weather"][0]["icon"],
                    "wind_speed": data["wind"]["speed"]
                }
                
                cache[cache_key] = result
                return result
                
            except httpx.TimeoutException:
                return {"error": "Сервис погоды временно недоступен", "city": city}
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 401:
                    return {"error": "Неверный API ключ"}
                elif e.response.status_code == 404:
                    return {"error": f"Город {city} не найден"}
                return {"error": f"Ошибка API: {e.response.status_code}"}
            except Exception as e:
                return {"error": str(e), "city": city}