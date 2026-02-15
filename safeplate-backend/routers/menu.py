from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.dish import Dish as DishModel
from models.allergen import DishAllergen
from pydantic import BaseModel

router = APIRouter()

class DishResponse(BaseModel):
    id: int
    name: str
    description: str
    allergens: List[str] = []
    
    class Config:
        from_attributes = True

class DishCreate(BaseModel):
    name: str
    description: str
    allergens: List[str] = []

@router.get("/", response_model=List[DishResponse])
def get_all_dishes(db: Session = Depends(get_db)):
    """Получить все блюда"""
    dishes = db.query(DishModel).all()
    
    result = []
    for dish in dishes:
        allergens = db.query(DishAllergen.allergen).filter(
            DishAllergen.dish_id == dish.id
        ).all()
        
        dish_data = DishResponse(
            id=dish.id,
            name=dish.name,
            description=dish.description or "",
            allergens=[a[0] for a in allergens]
        )
        result.append(dish_data)
    
    return result

@router.get("/{dish_id}", response_model=DishResponse)
def get_dish(dish_id: int, db: Session = Depends(get_db)):
    """Получить блюдо по ID"""
    dish = db.query(DishModel).filter(DishModel.id == dish_id).first()
    if not dish:
        raise HTTPException(status_code=404, detail="Dish not found")
    
    allergens = db.query(DishAllergen.allergen).filter(
        DishAllergen.dish_id == dish.id
    ).all()
    
    return DishResponse(
        id=dish.id,
        name=dish.name,
        description=dish.description or "",
        allergens=[a[0] for a in allergens]
    )

@router.post("/", response_model=DishResponse)
def create_dish(dish: DishCreate, db: Session = Depends(get_db)):
    """Создать новое блюдо"""
    new_dish = DishModel(
        name=dish.name,
        description=dish.description
    )
    db.add(new_dish)
    db.commit()
    db.refresh(new_dish)
    
    for allergen in dish.allergens:
        dish_allergen = DishAllergen(
            dish_id=new_dish.id,
            allergen=allergen
        )
        db.add(dish_allergen)
    
    db.commit()
    
    return DishResponse(
        id=new_dish.id,
        name=new_dish.name,
        description=new_dish.description or "",
        allergens=dish.allergens
    )

@router.delete("/{dish_id}")
def delete_dish(dish_id: int, db: Session = Depends(get_db)):
    """Удалить блюдо"""
    dish = db.query(DishModel).filter(DishModel.id == dish_id).first()
    if not dish:
        raise HTTPException(status_code=404, detail="Dish not found")
    

    db.query(DishAllergen).filter(DishAllergen.dish_id == dish_id).delete()
    
    db.delete(dish)
    db.commit()
    
    return {"message": "Dish deleted successfully"}

@router.get("/test")
def test():
    return {"message": "Menu router is working"}