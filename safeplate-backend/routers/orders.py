from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from database import get_db
from models.order import Order as OrderModel
from models.user import User as UserModel
from models.dish import Dish as DishModel
from schemas import OrderCreate, OrderResponse

router = APIRouter(tags=["Orders"])

@router.post("/", response_model=OrderResponse)
def create_order(data: OrderCreate, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == data.user_id).first()
    if not user:
        raise HTTPException(404, "User not found")
    
    for dish_id in data.dish_ids:
        dish = db.query(DishModel).filter(DishModel.id == dish_id).first()
        if not dish:
            raise HTTPException(404, f"Dish id {dish_id} not found")
    
    new_order = OrderModel(
        user_id=data.user_id,
        created_at=datetime.utcnow()
    )
    
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    
    return OrderResponse(
        id=new_order.id,
        user_id=new_order.user_id,
        dish_ids=data.dish_ids,
        created_at=new_order.created_at
    )

@router.get("/user/{user_id}", response_model=List[OrderResponse])
def get_user_orders(user_id: int, db: Session = Depends(get_db)):
    orders = db.query(OrderModel).filter(OrderModel.user_id == user_id).all()
    
    result = []
    for order in orders:
        result.append(OrderResponse(
            id=order.id,
            user_id=order.user_id,
            dish_ids=[],
            created_at=order.created_at
        ))
    
    return result

@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(OrderModel).filter(OrderModel.id == order_id).first()
    if not order:
        raise HTTPException(404, "Order not found")
    
    return OrderResponse(
        id=order.id,
        user_id=order.user_id,
        dish_ids=[],
        created_at=order.created_at
    )