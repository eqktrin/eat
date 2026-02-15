from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from database import get_db
from models.user import User as UserModel
from models.allergen import UserAllergen
from schemas import UserProfile
from dependencies import get_current_active_user
from models.user import User

router = APIRouter(tags=["Profile"])

class ProfileUpdateRequest(BaseModel):
    email: str
    allergens: List[str] = []

@router.get("/me", response_model=UserProfile)
def get_my_profile(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):

    allergens = db.query(UserAllergen.allergen).filter(
        UserAllergen.user_id == current_user.id
    ).all()
    
    return UserProfile(
        id=current_user.id,
        email=current_user.email,
        allergens=[a[0] for a in allergens]
    )

@router.put("/me", response_model=UserProfile)
def update_my_profile(
    data: ProfileUpdateRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    current_user.email = data.email
    db.commit()
    
    db.query(UserAllergen).filter(UserAllergen.user_id == current_user.id).delete()
    
    for allergen in data.allergens:
        user_allergen = UserAllergen(
            user_id=current_user.id,
            allergen=allergen
        )
        db.add(user_allergen)
    
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

    allergens = db.query(UserAllergen.allergen).filter(
        UserAllergen.user_id == user_id
    ).all()
    
    return UserProfile(
        id=user.id,
        email=user.email,
        allergens=[a[0] for a in allergens]
    )

@router.get("/debug/{user_id}")
def debug_profile(user_id: int, db: Session = Depends(get_db)):
    """Тестовый эндпоинт для отладки"""
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    
    if not user:
        return {"error": f"Пользователь с id={user_id} не найден"}
    
    allergens = db.query(UserAllergen.allergen).filter(
        UserAllergen.user_id == user_id
    ).all()
    
    allergens_list = [a[0] for a in allergens]
    
    return {
        "found": True,
        "id": user.id,
        "email": user.email,
        "allergens": allergens_list
    }