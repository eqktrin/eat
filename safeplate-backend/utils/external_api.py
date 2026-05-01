import httpx
import os
from cachetools import TTLCache
from dotenv import load_dotenv

load_dotenv()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"

# Кэш на 10 минут
cache = TTLCache(maxsize=100, ttl=600)

async def get_weather(city: str = "Moscow"):
    """Получить погоду для города"""
    
    # Проверяем кэш
    cache_key = f"weather_{city}"
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
                "temperature": data["main"]["temp"],
                "feels_like": data["main"]["feels_like"],
                "humidity": data["main"]["humidity"],
                "description": data["weather"][0]["description"],
                "icon": data["weather"][0]["icon"]
            }
            
            # Сохраняем в кэш
            cache[cache_key] = result
            return result
            
        except httpx.TimeoutException:
            return {"error": "Сервис погоды временно недоступен", "city": city}
        except httpx.HTTPStatusError as e:
            return {"error": f"Ошибка API: {e.response.status_code}", "city": city}
        except Exception as e:
            return {"error": str(e), "city": city}