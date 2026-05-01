from pydantic import BaseModel
from typing import List

class AllergensUpdate(BaseModel):
    user_id: int
    allergens: List[str]

class AllergyCheckResponse(BaseModel):
    dish_id: int
    user_id: int
    dangerous: bool
    conflicts: List[str]
