from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base

# Таблица для связи многие-ко-многим между блюдами и аллергенами
dish_allergen_association = Table(
    'dish_allergen_association',
    Base.metadata,
    Column('dish_id', Integer, ForeignKey('dishes.id')),
    Column('allergen_id', Integer, ForeignKey('allergens.id'))
)

# Таблица для связи многие-ко-многим между пользователями и аллергенами
user_allergen_association = Table(
    'user_allergen_association',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('allergen_id', Integer, ForeignKey('allergens.id'))
)

class Allergen(Base):
    __tablename__ = "allergens"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
    
    # Связи
    dishes = relationship("Dish", secondary=dish_allergen_association, back_populates="allergens")
    users = relationship("User", secondary=user_allergen_association, back_populates="allergens")