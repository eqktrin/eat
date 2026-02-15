from pydantic import BaseModel, EmailStr
from typing import List

class UserRegister(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserProfile(BaseModel):
    id: int
    email: EmailStr
    allergens: List[str] = []
