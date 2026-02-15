from pydantic import BaseModel
from typing import List


class OrderCreate(BaseModel):
    user_id: int
    dish_ids: List[int]

class OrderResponse(BaseModel):
    id: int
    user_id: int
    dish_ids: List[int]
