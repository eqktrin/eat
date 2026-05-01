# models/favorite.py
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Favorite(Base):
    __tablename__ = "favorites"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    dish_id = Column(Integer, ForeignKey("dishes.id"))
    
    # Связи
    user = relationship("User", back_populates="favorites")
    dish = relationship("Dish", back_populates="favorites")