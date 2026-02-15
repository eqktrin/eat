from database import SessionLocal
from models.dish import Dish
from models.allergen import DishAllergen

def add_more_dishes():
    db = SessionLocal()
    
    
    current_count = db.query(Dish).count()
    
    more_dishes = [
        # Завтраки
        {"name": "Блинчики с вареньем", "description": "Тонкие блинчики с малиновым вареньем", "allergens": ["gluten", "eggs", "dairy"]},
        {"name": "Йогурт с гранолой", "description": "Греческий йогурт с домашней гранолой", "allergens": ["dairy", "nuts"]},
        {"name": "Сырники", "description": "Творожные сырники со сметаной", "allergens": ["dairy", "gluten", "eggs"]},
        
        # Обеды
        {"name": "Курица терияки", "description": "Курица в сладком соусе терияки с рисом", "allergens": ["soy", "gluten"]},
        {"name": "Овощной суп", "description": "Легкий суп с сезонными овощами", "allergens": []},
        {"name": "Роллы Калифорния", "description": "С крабом, авокадо и огурцом", "allergens": ["fish", "soy"]},
        
        # Ужины
        {"name": "Лазанья", "description": "Слоеная паста с мясным соусом", "allergens": ["gluten", "dairy"]},
        {"name": "Стейк из лосося", "description": "На гриле с лимоном", "allergens": ["fish"]},
        {"name": "Рататуй", "description": "Французское овощное рагу", "allergens": []},
        
        # Десерты
        {"name": "Шоколадный торт", "description": "Нежный шоколадный бисквит", "allergens": ["gluten", "eggs", "dairy"]},
        {"name": "Яблочный пирог", "description": "С корицей и ванилью", "allergens": ["gluten", "dairy"]},
        {"name": "Мороженое", "description": "Ванильное мороженое", "allergens": ["dairy"]},
        
        # Веганские
        {"name": "Фалафель", "description": "Нутовые шарики с хумусом", "allergens": []},
        {"name": "Тофу с овощами", "description": "Жареный тофу с брокколи", "allergens": ["soy"]},
        {"name": "Киноа салат", "description": "С авокадо и томатами", "allergens": []},
    ]
    
    added_count = 0
    for dish_data in more_dishes:
        existing = db.query(Dish).filter(Dish.name == dish_data["name"]).first()
        if not existing:
            dish = Dish(
                name=dish_data["name"],
                description=dish_data["description"]
            )
            db.add(dish)
            db.commit()
            db.refresh(dish)
            
            for allergen in dish_data["allergens"]:
                dish_allergen = DishAllergen(
                    dish_id=dish.id,
                    allergen=allergen
                )
                db.add(dish_allergen)
            
            added_count += 1
            print(f"  ✅ Добавлено: {dish.name}")
    
    db.commit()
    print(f"\n Добавлено {added_count} новых блюд!")
    print(f" Всего блюд в БД: {db.query(Dish).count()}")
    
    db.close()

if __name__ == "__main__":
    add_more_dishes()