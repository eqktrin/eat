from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base

class UserAllergen(Base):
    __tablename__ = "user_allergens"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    allergen = Column(String)

class DishAllergen(Base):
    __tablename__ = "dish_allergens"
    
    id = Column(Integer, primary_key=True, index=True)
    dish_id = Column(Integer, ForeignKey("dishes.id"))
    allergen = Column(String)