from pydantic import BaseModel
from typing import List, Optional

class UserRegister(BaseModel):
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class DishCreate(BaseModel):
    name: str
    description: str
    allergens: List[str]

class DishUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    allergens: Optional[List[str]] = None

class AllergensUpdate(BaseModel):
    user_id: int
    allergens: List[str]
