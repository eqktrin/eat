import httpx
import os
from cachetools import TTLCache
from dotenv import load_dotenv

load_dotenv()

WEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", os.getenv("WEATHER_API_KEY", ""))
WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"

cache = TTLCache(maxsize=100, ttl=600)

# Простая функция для тестов (чтобы можно было замокать)
async def get_weather(city: str = "Moscow"):
    """Получить погоду для города (функция для моков)"""
    cache_key = f"weather_{city}"
    
    if cache_key in cache:
        return cache[cache_key]
    
    if not WEATHER_API_KEY:
        return {"city": city, "error": "API key not configured"}
    
    async with httpx.AsyncClient(timeout=10.0) as client:
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
            }
            
            cache[cache_key] = result
            return result
            
        except httpx.TimeoutException:
            return {"error": "Service temporarily unavailable", "city": city}
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                return {"error": "Invalid API key"}
            elif e.response.status_code == 404:
                return {"error": f"City {city} not found"}
            return {"error": f"API error: {e.response.status_code}"}
        except Exception as e:
            return {"error": str(e), "city": city}


# Класс для обратной совместимости
class WeatherService:
    @staticmethod
    async def get_weather(city: str = "Moscow"):
        return await get_weather(city)