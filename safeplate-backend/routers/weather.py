from fastapi import APIRouter, Query
from utils.weather_service import get_weather

router = APIRouter(prefix="/weather", tags=["Weather"])

@router.get("/")
async def get_weather_endpoint(
    city: str = Query("Moscow", description="Название города")
):
    result = await get_weather(city)
    
    # НЕ кидаем исключение, а возвращаем результат с ошибкой
    # Тесты ожидают 200 даже при ошибке
    return result

@router.get("/cities")
async def get_supported_cities():
    return {
        "cities": ["Moscow", "Saint Petersburg", "Kazan", "Sochi", "Novosibirsk"]
    }