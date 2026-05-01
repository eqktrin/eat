from fastapi import APIRouter, HTTPException, Query
from utils.weather_service import WeatherService

router = APIRouter(prefix="/weather", tags=["Weather"])

@router.get("/")
async def get_weather(
    city: str = Query("Moscow", description="Название города")
):

    result = await WeatherService.get_weather(city)
    
    if "error" in result:
        raise HTTPException(status_code=503, detail=result["error"])
    
    return result

@router.get("/cities")
async def get_supported_cities():
    return {
        "cities": ["Moscow", "Saint Petersburg", "Kazan", "Sochi", "Novosibirsk"]
    }