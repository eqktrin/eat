from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

#USER SCHEMAS
class UserRegister(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserProfile(BaseModel):
    id: int
    email: str
    allergens: List[str] = []

#DISH SCHEMAS
class DishBase(BaseModel):
    name: str
    description: str

class DishCreate(DishBase):
    allergens: List[str] = []

class DishResponse(DishBase):
    id: int
    allergens: List[str] = []

# ORDER SCHEMAS
class OrderCreate(BaseModel):
    user_id: int
    dish_ids: List[int]

class OrderResponse(BaseModel):
    id: int 
    user_id: int
    dish_ids: List[int]
    created_at: datetime

#FAVORITE SCHEMAS
class FavoriteRequest(BaseModel):
    user_id: int
    dish_id: int

#AI SCHEMAS
class AIQuery(BaseModel):
    query: str
    user_id: Optional[int] = None

class AIQueryResponse(BaseModel):
    dishes: List[DishResponse]
    reason: str