from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
import random
from database import get_db
from models.dish import Dish
from models.allergen import DishAllergen
from models.user import User
from models.allergen import UserAllergen
from schemas import DishResponse, AIQuery, AIQueryResponse

router = APIRouter()

@router.post("/query")
def ai_query(data: AIQuery, db: Session = Depends(get_db)):
    """AI рекомендации блюд с учетом аллергенов"""
    
    all_dishes = db.query(Dish).all()
    
    if not all_dishes:
        raise HTTPException(status_code=404, detail="В базе нет блюд")
    
    user_allergens = []
    if data.user_id:
        user = db.query(User).filter(User.id == data.user_id).first()
        if user:
            allergens = db.query(UserAllergen.allergen).filter(
                UserAllergen.user_id == data.user_id
            ).all()
            user_allergens = [a[0] for a in allergens]
    
    dishes_with_allergens = []
    for dish in all_dishes:
        dish_allergens = db.query(DishAllergen.allergen).filter(
            DishAllergen.dish_id == dish.id
        ).all()
        allergens_list = [a[0] for a in dish_allergens]
        
        dangerous = any(allergen in allergens_list for allergen in user_allergens)
        
        dishes_with_allergens.append({
            "dish": dish,
            "allergens": allergens_list,
            "dangerous": dangerous
        })
    
    query = data.query.lower()
    filtered_dishes = []
    
    if "сладк" in query or "сладеньк" in query or "десерт" in query:
        # Ищем десерты
        keywords = ["торт", "пирог", "мороженое", "блинчики", "варенье", "шоколад", "десерт"]
        for item in dishes_with_allergens:
            if any(keyword in item["dish"].name.lower() or keyword in item["dish"].description.lower() 
                   for keyword in keywords):
                if not item["dangerous"]: 
                    filtered_dishes.append(item)
        reason = " Подобраны сладкие блюда и десерты"
        
    elif "здор" in query or "полез" in query or "диет" in query:
        # Полезные блюда
        keywords = ["греч", "овощ", "салат", "фрукт", "куриц", "рыб", "полез", "диет"]
        for item in dishes_with_allergens:
            if any(keyword in item["dish"].name.lower() or keyword in item["dish"].description.lower() 
                   for keyword in keywords):
                if not item["dangerous"]:
                    filtered_dishes.append(item)
        reason = "Подобраны полезные и диетические блюда"
        
    elif "быстр" in query or "просто" in query:
        # Быстрые блюда
        keywords = ["салат", "суп", "омлет", "тост", "йогурт", "смузи", "быстр", "просто"]
        for item in dishes_with_allergens:
            if any(keyword in item["dish"].name.lower() or keyword in item["dish"].description.lower() 
                   for keyword in keywords):
                if not item["dangerous"]:
                    filtered_dishes.append(item)
        reason = "Подобраны быстрые в приготовлении блюда"
        
    elif "мяс" in query or "куриц" in query or "рыб" in query:
        # Мясные блюда
        keywords = ["куриц", "стейк", "лосос", "мяс", "рыб", "телятин", "говядин"]
        for item in dishes_with_allergens:
            if any(keyword in item["dish"].name.lower() or keyword in item["dish"].description.lower() 
                   for keyword in keywords):
                if not item["dangerous"]:
                    filtered_dishes.append(item)
        reason = " Подобраны мясные блюда"
        
    elif "веган" in query or "вегет" in query:
        # Веганские блюда
        keywords = ["веган", "тофу", "киноа", "фалафель", "рататуй", "овощ", "фрукт"]
        for item in dishes_with_allergens:
            if any(keyword in item["dish"].name.lower() or keyword in item["dish"].description.lower() 
                   for keyword in keywords):
                if not item["dangerous"]:
                    filtered_dishes.append(item)
        reason = "Подобраны веганские блюда"
        
    else:
        safe_dishes = [item for item in dishes_with_allergens if not item["dangerous"]]
        if len(safe_dishes) >= 3:
            filtered_dishes = random.sample(safe_dishes, 3)
        else:
            filtered_dishes = safe_dishes
        reason = f" Подобраны блюда по запросу: '{query}'"
    
    if not filtered_dishes:
        safe_dishes = [item for item in dishes_with_allergens if not item["dangerous"]]
        if safe_dishes:
            filtered_dishes = random.sample(safe_dishes, min(3, len(safe_dishes)))
            reason = " Подобраны популярные безопасные блюда"
        else:
            filtered_dishes = random.sample(dishes_with_allergens, min(3, len(dishes_with_allergens)))
            reason = " Внимание! Некоторые блюда могут содержать аллергены"
    
 
    response_dishes = []
    for item in filtered_dishes[:5]: 
        response_dishes.append(DishResponse(
            id=item["dish"].id,
            name=item["dish"].name,
            description=item["dish"].description,
            allergens=item["allergens"]
        ))
    
    return AIQueryResponse(dishes=response_dishes, reason=reason)

@router.get("/test")
def test():
    return {"message": "AI router is working"}