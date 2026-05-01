from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List, Optional
import random
from database import get_db
from models.dish import Dish, DishCategory
from models.allergen import Allergen, dish_allergen_association, user_allergen_association
from models.user import User
from schemas import DishResponse, AIQuery, AIQueryResponse

router = APIRouter()

# Ключевые слова для исключения (если нет категории)
MEAT_KEYWORDS = ["мяс", "куриц", "говяд", "свин", "баранин", "котлет", "фарш", "ветчин", "бекон", "пельмен", "шашлык"]
FISH_KEYWORDS = ["рыб", "лосос", "семг", "тунц", "кревет", "миди", "кальмар", "морепр", "уха"]
DAIRY_KEYWORDS = ["молок", "сливк", "сыр", "творог", "сметан", "йогурт", "масл"]
EGG_KEYWORDS = ["яйц", "яичн", "омлет"]

@router.post("/query")
def ai_query(data: AIQuery, db: Session = Depends(get_db)):
    """AI рекомендации блюд с учетом аллергенов и категорий"""
    
    all_dishes = db.query(Dish).all()
    
    if not all_dishes:
        raise HTTPException(status_code=404, detail="В базе нет блюд")
    
    # Получаем аллергены пользователя
    user_allergens = []
    if data.user_id:
        result = db.execute(
            select(Allergen.name)
            .select_from(user_allergen_association)
            .join(Allergen, Allergen.id == user_allergen_association.c.allergen_id)
            .where(user_allergen_association.c.user_id == data.user_id)
        )
        user_allergens = [row[0] for row in result]
    
    # Обогащаем блюда аллергенами
    dishes_with_allergens = []
    for dish in all_dishes:
        result = db.execute(
            select(Allergen.name)
            .select_from(dish_allergen_association)
            .join(Allergen, Allergen.id == dish_allergen_association.c.allergen_id)
            .where(dish_allergen_association.c.dish_id == dish.id)
        )
        allergens_list = [row[0] for row in result]
        
        dangerous = any(a in allergens_list for a in user_allergens)
        
        dishes_with_allergens.append({
            "dish": dish,
            "allergens": allergens_list,
            "dangerous": dangerous,
            "category": dish.category.value if dish.category else None,
            "text": (dish.name + " " + (dish.description or "")).lower()
        })
    
    query = data.query.lower()
    filtered_dishes = []
    
    # ========== ПОИСК ПО КАТЕГОРИЯМ ==========
    
    if "суп" in query or "супы" in query:
        filtered_dishes = [d for d in dishes_with_allergens 
                          if d["category"] == DishCategory.SOUP.value and not d["dangerous"]]
        reason = "🥣 Подобраны супы"
    
    elif "салат" in query:
        filtered_dishes = [d for d in dishes_with_allergens 
                          if d["category"] == DishCategory.SALAD.value and not d["dangerous"]]
        reason = "🥗 Подобраны салаты"
    
    elif "десерт" in query or "сладк" in query or "торт" in query:
        filtered_dishes = [d for d in dishes_with_allergens 
                          if d["category"] == DishCategory.DESSERT.value and not d["dangerous"]]
        reason = "🍰 Подобраны десерты"
    
    elif "мяс" in query:
        filtered_dishes = [d for d in dishes_with_allergens 
                          if d["category"] == DishCategory.MEAT.value and not d["dangerous"]]
        reason = "🥩 Подобраны мясные блюда"
    
    elif "рыб" in query or "море" in query:
        filtered_dishes = [d for d in dishes_with_allergens 
                          if d["category"] == DishCategory.FISH.value and not d["dangerous"]]
        reason = "🐟 Подобраны рыбные блюда и морепродукты"
    
    elif "веган" in query or "вегет" in query or "пост" in query:
        # Веганские блюда — строго по категории VEGAN
        filtered_dishes = [d for d in dishes_with_allergens 
                          if d["category"] == DishCategory.VEGAN.value and not d["dangerous"]]
        
        if filtered_dishes:
            reason = "🌱 Подобраны веганские блюда"
        else:
            # Если веганских нет — показываем овощные (SALAD, SIDE_DISH без мяса/молока)
            veg_fallback = []
            for d in dishes_with_allergens:
                if d["dangerous"]:
                    continue
                cat = d["category"]
                if cat in [DishCategory.SALAD.value, DishCategory.SIDE_DISH.value]:
                    # Дополнительно проверяем на наличие мяса/рыбы в тексте
                    if not any(k in d["text"] for k in MEAT_KEYWORDS + FISH_KEYWORDS + DAIRY_KEYWORDS + EGG_KEYWORDS):
                        veg_fallback.append(d)
            filtered_dishes = veg_fallback
            reason = "🥬 Подобраны овощные блюда (веганских нет)"
    
    elif "напит" in query or "пить" in query or "чай" in query or "кофе" in query or "сок" in query:
        filtered_dishes = [d for d in dishes_with_allergens 
                          if d["category"] == DishCategory.DRINK.value and not d["dangerous"]]
        
        if filtered_dishes:
            reason = "🥤 Подобраны напитки"
        else:
            reason = "🥤 Напитков нет, показываем безопасные блюда"
    
    elif "гарнир" in query:
        filtered_dishes = [d for d in dishes_with_allergens 
                          if d["category"] == DishCategory.SIDE_DISH.value and not d["dangerous"]]
        reason = "🍚 Подобраны гарниры"
    
    else:
        # ========== ЕСЛИ КАТЕГОРИЯ НЕ ОПРЕДЕЛЕНА ==========
        # Ищем ключевые слова в тексте
        words = query.split()
        for d in dishes_with_allergens:
            if d["dangerous"]:
                continue
            if any(word in d["text"] for word in words if len(word) > 2):
                filtered_dishes.append(d)
        
        if filtered_dishes:
            reason = f"🔍 Подобраны блюда по запросу: '{data.query}'"
        else:
            # Если ничего не нашли — случайные безопасные
            safe = [d for d in dishes_with_allergens if not d["dangerous"]]
            filtered_dishes = random.sample(safe, min(3, len(safe))) if safe else []
            reason = "🍽️ Подобраны популярные безопасные блюда"
    
      # ========== ЗАПАСНОЙ ВАРИАНТ ==========
    if not filtered_dishes:
        safe = [d for d in dishes_with_allergens if not d["dangerous"]]
        # Исключаем десерты и жирное из "полезного"
        if "полез" in query:
            safe = [d for d in safe if d["category"] not in [DishCategory.DESSERT.value, DishCategory.MAIN.value]]
        filtered_dishes = random.sample(safe, min(3, len(safe))) if safe else []
        reason = "🍽️ Подобраны популярные безопасные блюда"
    # Формируем ответ
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