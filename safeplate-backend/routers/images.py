from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from database import get_db
from models.dish import Dish
from models.dish_image import DishImage
from dependencies import get_current_user, require_role
from models.user import User, UserRole
from utils.upload import save_file, delete_file
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/images", tags=["images"])

@router.post("/upload/{dish_id}")
async def upload_dish_image(
    dish_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.ADMIN))
):
    
    dish = db.query(Dish).filter(Dish.id == dish_id).first()
    if not dish:
        raise HTTPException(status_code=404, detail="Блюдо не найдено")
    
    file_content = await file.read()
    
    try:
        file_info = save_file(file_content, file.filename)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    db_image = DishImage(
        dish_id=dish_id,
        image_url=file_info["url"],
        file_name=file_info["file_name"],
        file_size=file_info["file_size"],
        content_type=file_info["content_type"]
    )
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    
    logger.info(f"Загружено изображение для блюда {dish_id}: {file_info['url']}")
    
    return {
        "id": db_image.id,
        "url": db_image.image_url,
        "file_name": db_image.file_name,
        "file_size": db_image.file_size
    }

@router.get("/{image_id}")
def get_image_info(
    image_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    
    image = db.query(DishImage).filter(DishImage.id == image_id).first()
    if not image:
        raise HTTPException(status_code=404, detail="Изображение не найдено")
    
    return {
        "id": image.id,
        "url": image.image_url,
        "file_name": image.file_name,
        "file_size": image.file_size,
        "created_at": image.created_at
    }

@router.delete("/{image_id}")
def delete_image(
    image_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.ADMIN))
):
    
    image = db.query(DishImage).filter(DishImage.id == image_id).first()
    if not image:
        raise HTTPException(status_code=404, detail="Изображение не найдено")
    
    delete_file(image.image_url)
    
    db.delete(image)
    db.commit()
    
    return {"message": "Изображение удалено"}