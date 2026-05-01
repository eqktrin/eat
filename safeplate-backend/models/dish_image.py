from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class DishImage(Base):
    __tablename__ = "dish_images"
    
    id = Column(Integer, primary_key=True, index=True)
    dish_id = Column(Integer, ForeignKey("dishes.id"), nullable=False)
    image_url = Column(String, nullable=False)
    file_name = Column(String, nullable=False)
    file_size = Column(Integer, nullable=True)
    content_type = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    dish = relationship("Dish", back_populates="images")