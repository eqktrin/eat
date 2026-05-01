# clean_all.py
import os
import shutil
from database import SessionLocal
from models.dish_image import DishImage
from models.dish import Dish
from models.user import User
from models.favorite import Favorite
from models.order import Order
from models.allergen import Allergen

def clean_everything():
    db = SessionLocal()
    
    # 1. Очищаем таблицу картинок
    deleted_images = db.query(DishImage).delete()
    print(f"Удалено картинок из БД: {deleted_images}")
    
    # 2. Очищаем папку uploads
    uploads_dir = "uploads"
    if os.path.exists(uploads_dir):
        shutil.rmtree(uploads_dir)
        os.makedirs(uploads_dir)
        print(f"Папка {uploads_dir} очищена")
    
    # 3. Очищаем другие таблицы (по желанию)
    # db.query(Favorite).delete()
    # db.query(Order).delete()
    
    db.commit()
    db.close()
    
    print("✅ Готово! Всё очищено.")

if __name__ == "__main__":
    clean_everything()