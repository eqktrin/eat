from sqlalchemy import Column, Integer, String, Text, Enum
from sqlalchemy.orm import relationship
from database import Base
import enum

class DishCategory(str, enum.Enum):
    SOUP = "soup"              # Супы
    MAIN = "main"               # Основные блюда
    SALAD = "salad"             # Салаты
    DESSERT = "dessert"         # Десерты
    VEGAN = "vegan"             # Веганские блюда
    MEAT = "meat"               # Мясные блюда
    FISH = "fish"               # Рыбные блюда
    SIDE_DISH = "side_dish"     # Гарниры
    DRINK = "drink"             # Напитки
    BAKERY = "bakery"           # Выпечка

class Dish(Base):
    __tablename__ = "dishes"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    category = Column(Enum(DishCategory), default=DishCategory.MAIN, nullable=False)
    
    # Связи
    allergens = relationship("Allergen", secondary="dish_allergen_association", back_populates="dishes")
    favorites = relationship("Favorite", back_populates="dish")
    images = relationship("DishImage", back_populates="dish", cascade="all, delete-orphan")