from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from pydantic import BaseModel
from typing import List
from database import get_db
from models.allergen import Allergen, user_allergen_association
from dependencies import get_current_active_user
from models.user import User

router = APIRouter()

KNOWN_ALLERGENS = ["dairy", "gluten", "eggs", "berries", "nuts", "soy", "fish", "shellfish"]

class AllergensUpdateRequest(BaseModel):
    allergens: List[str] = []


@router.get("/")
def get_known_allergens():
    """Получить список известных аллергенов"""
    return {"allergens": KNOWN_ALLERGENS}


@router.get("/my")
def get_my_allergens(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Получить аллергены текущего пользователя"""
    result = db.execute(
        select(Allergen.name)
        .select_from(user_allergen_association)
        .join(Allergen, Allergen.id == user_allergen_association.c.allergen_id)
        .where(user_allergen_association.c.user_id == current_user.id)
    )
    allergens = [row[0] for row in result]
    
    return {
        "user_id": current_user.id,
        "allergens": allergens
    }


@router.post("/update")
def update_my_allergens(
    data: AllergensUpdateRequest,
    current_user: User = Depends(get_current_active_user),  
    db: Session = Depends(get_db)
):
    """Обновить аллергены текущего пользователя"""
    # Удаляем дубликаты
    unique_allergens = list(set(data.allergens))
    
    # Удаляем старые связи
    db.execute(
        user_allergen_association.delete().where(
            user_allergen_association.c.user_id == current_user.id
        )
    )
    
    # Добавляем новые аллергены
    for allergen_name in unique_allergens:
        allergen = db.query(Allergen).filter(Allergen.name == allergen_name).first()
        if not allergen:
            allergen = Allergen(name=allergen_name)
            db.add(allergen)
            db.flush()
        
        db.execute(
            user_allergen_association.insert().values(
                user_id=current_user.id,
                allergen_id=allergen.id
            )
        )
    
    db.commit()
    
    return {
        "message": "Allergens updated",
        "user_id": current_user.id,
        "allergens": unique_allergens,
    }