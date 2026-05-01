from fastapi import APIRouter, HTTPException
from utils.external_api import get_weather

router = APIRouter(prefix="/external", tags=["External API"])

@router.get("/weather")
async def weather(city: str = "Moscow"):
    """Получить погоду (кэшируется на 10 минут)"""
    result = await get_weather(city)
    
    if "error" in result:
        raise HTTPException(status_code=503, detail=result["error"])
    
    return result