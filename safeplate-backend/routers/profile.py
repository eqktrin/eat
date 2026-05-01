from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from pydantic import BaseModel
from typing import List
from database import get_db
from models.user import User as UserModel
from models.allergen import Allergen, user_allergen_association
from schemas import UserProfile
from dependencies import get_current_active_user
from models.user import User

router = APIRouter()

class ProfileUpdateRequest(BaseModel):
    email: str
    allergens: List[str] = []

@router.get("/me", response_model=UserProfile)
def get_my_profile(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # Получаем аллергены пользователя
    result = db.execute(
        select(Allergen.name)
        .select_from(user_allergen_association)
        .join(Allergen, Allergen.id == user_allergen_association.c.allergen_id)
        .where(user_allergen_association.c.user_id == current_user.id)
    )
    allergens = [row[0] for row in result]
    
    return UserProfile(
        id=current_user.id,
        email=current_user.email,
        allergens=allergens
    )

@router.put("/me", response_model=UserProfile)
def update_my_profile(
    data: ProfileUpdateRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # Обновляем email
    current_user.email = data.email
    
    # Удаляем старые связи с аллергенами
    db.execute(
        user_allergen_association.delete().where(
            user_allergen_association.c.user_id == current_user.id
        )
    )
    
    # Добавляем новые аллергены
    for allergen_name in data.allergens:
        # Находим или создаем аллерген
        allergen = db.query(Allergen).filter(Allergen.name == allergen_name).first()
        if not allergen:
            allergen = Allergen(name=allergen_name)
            db.add(allergen)
            db.flush()
        
        # Создаем связь
        db.execute(
            user_allergen_association.insert().values(
                user_id=current_user.id,
                allergen_id=allergen.id
            )
        )
    
    db.commit()
    
    return UserProfile(
        id=current_user.id,
        email=current_user.email,
        allergens=data.allergens
    )

@router.get("/{user_id}", response_model=UserProfile)
def get_profile(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(404, "User not found")

    # Получаем аллергены пользователя
    result = db.execute(
        select(Allergen.name)
        .select_from(user_allergen_association)
        .join(Allergen, Allergen.id == user_allergen_association.c.allergen_id)
        .where(user_allergen_association.c.user_id == user_id)
    )
    allergens = [row[0] for row in result]
    
    return UserProfile(
        id=user.id,
        email=user.email,
        allergens=allergens
    )

@router.get("/debug/{user_id}")
def debug_profile(user_id: int, db: Session = Depends(get_db)):
    """Тестовый эндпоинт для отладки"""
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    
    if not user:
        return {"error": f"Пользователь с id={user_id} не найден"}
    
    # Получаем аллергены пользователя
    result = db.execute(
        select(Allergen.name)
        .select_from(user_allergen_association)
        .join(Allergen, Allergen.id == user_allergen_association.c.allergen_id)
        .where(user_allergen_association.c.user_id == user_id)
    )
    allergens = [row[0] for row in result]
    
    return {
        "found": True,
        "id": user.id,
        "email": user.email,
        "allergens": allergens
    }