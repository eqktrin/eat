from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from database import get_db
from models.allergen import UserAllergen
from dependencies import get_current_active_user
from models.user import User

router = APIRouter(tags=["Allergens"])

KNOWN_ALLERGENS = ["dairy", "gluten", "eggs", "berries", "nuts", "soy", "fish", "shellfish"]

class AllergensUpdateRequest(BaseModel):
    allergens: List[str] = []

class AllergensUpdateOld(BaseModel):
    user_id: int
    allergens: List[str] = []

@router.get("/")
def get_known_allergens():
    return {"allergens": KNOWN_ALLERGENS}

@router.get("/my")
def get_my_allergens(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    allergens = db.query(UserAllergen.allergen).filter(
        UserAllergen.user_id == current_user.id
    ).all()
    
    return {
        "user_id": current_user.id,
        "allergens": [a[0] for a in allergens]
    }

@router.post("/update")
def update_my_allergens(
    data: AllergensUpdateRequest,
    current_user: User = Depends(get_current_active_user),  
    db: Session = Depends(get_db)
):

    db.query(UserAllergen).filter(UserAllergen.user_id == current_user.id).delete()
    

    for allergen in data.allergens:
        user_allergen = UserAllergen(
            user_id=current_user.id, 
            allergen=allergen
        )
        db.add(user_allergen)
    
    db.commit()
    
    return {
        "message": "Allergens updated",
        "user_id": current_user.id,
        "allergens": data.allergens,
    }

@router.post("/update-old")
def update_user_allergens_old(
    data: AllergensUpdateOld,  
    db: Session = Depends(get_db)
):
    db.query(UserAllergen).filter(UserAllergen.user_id == data.user_id).delete()
    
    for allergen in data.allergens:
        user_allergen = UserAllergen(
            user_id=data.user_id,
            allergen=allergen
        )
        db.add(user_allergen)
    
    db.commit()
    
    return {
        "message": "Allergens updated",
        "user_id": data.user_id,
        "allergens": data.allergens,
    }