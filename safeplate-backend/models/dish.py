from sqlalchemy import Column, Integer, String, Text
from database import Base

class Dish(Base):
    __tablename__ = "dishes"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)