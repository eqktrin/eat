from pydantic import BaseModel
from typing import List, Optional


class DishCreate(BaseModel):
    name: str
    description: str
    allergens: List[str] = []

class DishUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    allergens: Optional[List[str]] = None

class DishResponse(BaseModel):
    id: int
    name: str
    description: str
    allergens: List[str]
