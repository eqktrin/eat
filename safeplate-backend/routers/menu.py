from fastapi import APIRouter, Depends, HTTPException, status, Query, Response
from sqlalchemy.orm import Session
from sqlalchemy import select, or_
from typing import List, Optional
from models.allergen import Allergen, dish_allergen_association, user_allergen_association
from models.dish_image import DishImage
from database import get_db
from models.dish import Dish as DishModel, DishCategory
from models.user import User, UserRole
from dependencies import require_role, get_current_user
from pydantic import BaseModel

router = APIRouter()

class DishResponse(BaseModel):
    id: int
    name: str
    description: str
    allergens: List[str] = []
    category: Optional[str] = None
    images: List[dict] = []

    class Config:
        from_attributes = True

class DishCreate(BaseModel):
    name: str
    description: str
    allergens: List[str] = []
    category: Optional[str] = None

class DishUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    allergens: Optional[List[str]] = None
    category: Optional[str] = None

@router.get("/", response_model=List[DishResponse])
def get_all_dishes(
    response: Response,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    
    search: Optional[str] = Query(None, description="Поиск по названию"),
    
    category: Optional[str] = Query(None, description="Фильтр по категории"),
    
    safe_only: Optional[bool] = Query(False, description="Только безопасные (без аллергенов пользователя)"),

    sort_by: Optional[str] = Query("name", description="Поле для сортировки (name, category)"),
    sort_order: Optional[str] = Query("asc", description="Направление (asc, desc)"),

    skip: int = Query(0, ge=0, description="Сколько пропустить"),
    limit: int = Query(10, ge=1, le=100, description="Сколько вернуть")
    
):
    query = db.query(DishModel)

    if search:
        query = query.filter(DishModel.name.ilike(f"%{search}%"))
    
    if category:
        query = query.filter(DishModel.category == category)
    
    user_allergen_names = []
    if safe_only and current_user:
        user_allergens = db.execute(
            select(Allergen.name)
            .select_from(user_allergen_association)
            .join(Allergen, Allergen.id == user_allergen_association.c.allergen_id)
            .where(user_allergen_association.c.user_id == current_user.id)
        )
        user_allergen_names = [row[0] for row in user_allergens]
    
    if sort_by == "name":
        if sort_order == "desc":
            query = query.order_by(DishModel.name.desc())
        else:
            query = query.order_by(DishModel.name.asc())
    elif sort_by == "category":
        if sort_order == "desc":
            query = query.order_by(DishModel.category.desc())
        else:
            query = query.order_by(DishModel.category.asc())
    else:
        query = query.order_by(DishModel.name.asc())
    
    total = query.count()
    dishes = query.offset(skip).limit(limit).all()
    
    result = []
    for dish in dishes:
        dish_allergens = db.execute(
            select(Allergen.name)
            .select_from(dish_allergen_association)
            .join(Allergen, Allergen.id == dish_allergen_association.c.allergen_id)
            .where(dish_allergen_association.c.dish_id == dish.id)
        )
        allergens = [row[0] for row in dish_allergens]
        
        dish_images = db.query(DishImage).filter(DishImage.dish_id == dish.id).all()
        images_data = [
            {"id": img.id, "image_url": img.image_url}
            for img in dish_images
        ]
        
        if safe_only and user_allergen_names:
            if any(a in user_allergen_names for a in allergens):
                continue
        
        result.append(
            DishResponse(
                id=dish.id,
                name=dish.name,
                description=dish.description or "",
                allergens=allergens,
                category=dish.category.value if dish.category else None,
                images=images_data
            )
        )
    
    response.headers["X-Total-Count"] = str(total)
    
    return result

@router.get("/{dish_id}", response_model=DishResponse)
def get_dish(
    dish_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    dish = db.query(DishModel).filter(DishModel.id == dish_id).first()
    if not dish:
        raise HTTPException(status_code=404, detail="Dish not found")

    dish_allergens = db.execute(
        select(Allergen.name)
        .select_from(dish_allergen_association)
        .join(Allergen, Allergen.id == dish_allergen_association.c.allergen_id)
        .where(dish_allergen_association.c.dish_id == dish.id)
    )
    allergens = [row[0] for row in dish_allergens]
    
    dish_images = db.query(DishImage).filter(DishImage.dish_id == dish.id).all()
    images_data = [
        {"id": img.id, "image_url": img.image_url}
        for img in dish_images
    ]

    return DishResponse(
        id=dish.id,
        name=dish.name,
        description=dish.description or "",
        allergens=allergens,
        category=dish.category.value if dish.category else None,
        images=images_data
    )

@router.post("/", response_model=DishResponse, dependencies=[Depends(require_role(UserRole.ADMIN))])
def create_dish(
    dish: DishCreate,
    db: Session = Depends(get_db)
):
    new_dish = DishModel(
        name=dish.name,
        description=dish.description,
        category=dish.category
    )
    db.add(new_dish)
    db.flush()

    for allergen_name in dish.allergens:
        allergen = db.query(Allergen).filter(Allergen.name == allergen_name).first()
        if not allergen:
            allergen = Allergen(name=allergen_name)
            db.add(allergen)
            db.flush()

        db.execute(
            dish_allergen_association.insert().values(
                dish_id=new_dish.id,
                allergen_id=allergen.id
            )
        )

    db.commit()
    db.refresh(new_dish)

    return DishResponse(
        id=new_dish.id,
        name=new_dish.name,
        description=new_dish.description or "",
        allergens=dish.allergens,
        category=dish.category,
        images=[]
    )

@router.put("/{dish_id}", response_model=DishResponse, dependencies=[Depends(require_role(UserRole.ADMIN))])
def update_dish(
    dish_id: int,
    dish_data: DishUpdate,
    db: Session = Depends(get_db)
):
    dish = db.query(DishModel).filter(DishModel.id == dish_id).first()
    if not dish:
        raise HTTPException(status_code=404, detail="Dish not found")
    
    if dish_data.name is not None:
        dish.name = dish_data.name
    if dish_data.description is not None:
        dish.description = dish_data.description
    if dish_data.category is not None:
        dish.category = dish_data.category
    
    if dish_data.allergens is not None:
        db.execute(
            dish_allergen_association.delete().where(
                dish_allergen_association.c.dish_id == dish_id
            )
        )
        
        for allergen_name in dish_data.allergens:
            allergen = db.query(Allergen).filter(Allergen.name == allergen_name).first()
            if not allergen:
                allergen = Allergen(name=allergen_name)
                db.add(allergen)
                db.flush()
            
            db.execute(
                dish_allergen_association.insert().values(
                    dish_id=dish_id,
                    allergen_id=allergen.id
                )
            )
    
    db.commit()
    db.refresh(dish)
    
    dish_allergens = db.execute(
        select(Allergen.name)
        .select_from(dish_allergen_association)
        .join(Allergen, Allergen.id == dish_allergen_association.c.allergen_id)
        .where(dish_allergen_association.c.dish_id == dish.id)
    )
    allergens = [row[0] for row in dish_allergens]
    
    dish_images = db.query(DishImage).filter(DishImage.dish_id == dish.id).all()
    images_data = [
        {"id": img.id, "image_url": img.image_url}
        for img in dish_images
    ]
    
    return DishResponse(
        id=dish.id,
        name=dish.name,
        description=dish.description or "",
        allergens=allergens,
        category=dish.category.value if dish.category else None,
        images=images_data
    )

@router.delete("/{dish_id}", dependencies=[Depends(require_role(UserRole.ADMIN))]) 
def delete_dish(
    dish_id: int,
    db: Session = Depends(get_db)
):
    dish = db.query(DishModel).filter(DishModel.id == dish_id).first()
    if not dish:
        raise HTTPException(status_code=404, detail="Dish not found")

    db.execute(
        dish_allergen_association.delete().where(
            dish_allergen_association.c.dish_id == dish_id
        )
    )

    db.delete(dish)
    db.commit()

    return {"message": "Dish deleted successfully"}

@router.get("/test")
def test():
    return {"message": "Menu router is working"}
