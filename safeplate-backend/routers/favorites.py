from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List
from database import get_db
from models.favorite import Favorite as FavoriteModel
from models.dish import Dish as DishModel
from models.allergen import Allergen, dish_allergen_association
from schemas import DishResponse
from dependencies import get_current_active_user
from models.user import User
from pydantic import BaseModel

router = APIRouter()

class FavoriteAddRequest(BaseModel):
    dish_id: int

class FavoriteRemoveRequest(BaseModel):
    dish_id: int

@router.post("/add")
def add_favorite(
    data: FavoriteAddRequest,
    current_user: User = Depends(get_current_active_user), 
    db: Session = Depends(get_db)
):
    dish = db.query(DishModel).filter(DishModel.id == data.dish_id).first()
    if not dish:
        raise HTTPException(404, "Dish not found")
    
    existing = db.query(FavoriteModel).filter(
        FavoriteModel.user_id == current_user.id, 
        FavoriteModel.dish_id == data.dish_id
    ).first()
    
    if existing:
        return {"message": "Dish already in favorites"}
    
    new_favorite = FavoriteModel(
        user_id=current_user.id, 
        dish_id=data.dish_id
    )
    
    db.add(new_favorite)
    db.commit()
    
    return {
        "message": "Dish added to favorites",
        "dish_id": data.dish_id,
        "user_id": current_user.id
    }

@router.get("/my", response_model=List[DishResponse])
def get_my_favorites(
    current_user: User = Depends(get_current_active_user), 
    db: Session = Depends(get_db)
):
    favorite_ids = db.query(FavoriteModel.dish_id).filter(
        FavoriteModel.user_id == current_user.id 
    ).all()
    
    if not favorite_ids:
        return []
    
    dish_ids = [fid[0] for fid in favorite_ids]
    dishes = db.query(DishModel).filter(DishModel.id.in_(dish_ids)).all()
    
    result = []
    for dish in dishes:
        # Получаем аллергены блюда
        result_allergens = db.execute(
            select(Allergen.name)
            .select_from(dish_allergen_association)
            .join(Allergen, Allergen.id == dish_allergen_association.c.allergen_id)
            .where(dish_allergen_association.c.dish_id == dish.id)
        )
        allergens = [row[0] for row in result_allergens]
        
        dish_data = DishResponse(
            id=dish.id,
            name=dish.name,
            description=dish.description or "",
            allergens=allergens
        )
        result.append(dish_data)
    
    return result

@router.post("/remove")
def remove_favorite(
    data: FavoriteRemoveRequest,
    current_user: User = Depends(get_current_active_user), 
    db: Session = Depends(get_db)
):
    favorite = db.query(FavoriteModel).filter(
        FavoriteModel.user_id == current_user.id,  
        FavoriteModel.dish_id == data.dish_id
    ).first()
    
    if not favorite:
        raise HTTPException(404, "Dish not in favorites")
    
    db.delete(favorite)
    db.commit()
    
    return {
        "message": "Dish removed from favorites",
        "dish_id": data.dish_id,
        "user_id": current_user.id
    }