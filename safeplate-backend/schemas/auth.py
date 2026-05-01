from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from models.user import UserRole

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class OAuth2PasswordRequestFormCustom(BaseModel):
    username: str 
    password: str
    grant_type: Optional[str] = None
    scope: str = ""
    client_id: Optional[str] = None
    client_secret: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[int] = None

class UserResponse(UserBase):
    id: int
    role: UserRole
    
    class Config:
        from_attributes = True