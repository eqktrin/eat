# add_dishes.py
from database import SessionLocal
from models.dish import Dish, DishCategory
from models.allergen import Allergen, dish_allergen_association

def add_sample_dishes():
    db = SessionLocal()
    
    print("🍽️  Начинаем наполнение базы данных...")
    print("=" * 60)
    
    # Создадим аллергены
    allergens_data = [
        {"name": "dairy", "description": "Молочные продукты (лактоза)"},
        {"name": "gluten", "description": "Глютен (пшеница, рожь, ячмень)"},
        {"name": "nuts", "description": "Орехи (грецкие, миндаль, фундук)"},
        {"name": "eggs", "description": "Яйца"},
        {"name": "fish", "description": "Рыба и морепродукты"},
        {"name": "soy", "description": "Соя"},
        {"name": "sesame", "description": "Кунжут"},
        {"name": "mustard", "description": "Горчица"},
        {"name": "celery", "description": "Сельдерей"},
        {"name": "sulfites", "description": "Сульфиты (консерванты)"},
    ]
    
    allergens = {}
    for a_data in allergens_data:
        allergen = db.query(Allergen).filter(Allergen.name == a_data["name"]).first()
        if not allergen:
            allergen = Allergen(**a_data)
            db.add(allergen)
            db.flush()
            print(f"✅ Создан аллерген: {a_data['name']} - {a_data['description']}")
        else:
            print(f"⏩ Аллерген уже существует: {a_data['name']}")
        allergens[a_data["name"]] = allergen
    
    print("=" * 60)
    
    # 🔥 МЕГА-СПИСОК БЛЮД (50+ штук) с КАТЕГОРИЯМИ
    dishes_data = [
        # СУПЫ (10)
        {
            "name": "Борщ украинский",
            "description": "Традиционный суп со свеклой, капустой и мясом. Подается со сметаной",
            "category": DishCategory.SOUP,
            "allergens": ["dairy"]
        },
        {
            "name": "Солянка сборная",
            "description": "Суп с колбасами, солеными огурцами, оливками и лимоном",
            "category": DishCategory.SOUP,
            "allergens": []
        },
        {
            "name": "Крем-суп из шампиньонов",
            "description": "Нежный суп с грибами и сливками",
            "category": DishCategory.SOUP,
            "allergens": ["dairy"]
        },
        {
            "name": "Том Ям",
            "description": "Тайский острый суп с креветками на кокосовом молоке",
            "category": DishCategory.SOUP,
            "allergens": ["fish", "dairy"]
        },
        {
            "name": "Мисо-суп",
            "description": "Японский суп с тофу и водорослями",
            "category": DishCategory.SOUP,
            "allergens": ["soy", "fish"]
        },
        {
            "name": "Куриный суп с лапшой",
            "description": "Домашний куриный суп с яичной лапшой",
            "category": DishCategory.SOUP,
            "allergens": ["gluten", "eggs"]
        },
        {
            "name": "Гаспачо",
            "description": "Холодный испанский суп из помидоров и овощей",
            "category": DishCategory.SOUP,
            "allergens": []
        },
        {
            "name": "Французский луковый суп",
            "description": "Суп с сырной корочкой и гренками",
            "category": DishCategory.SOUP,
            "allergens": ["dairy", "gluten"]
        },
        {
            "name": "Уха царская",
            "description": "Рыбный суп из лосося с овощами",
            "category": DishCategory.SOUP,
            "allergens": ["fish"]
        },
        {
            "name": "Чечевичный суп",
            "description": "Сытный суп из красной чечевицы с тмином",
            "category": DishCategory.SOUP,
            "allergens": []
        },
        
        # ГАРНИРЫ
        {
            "name": "Гречка с грибами",
            "description": "Рассчытчатая гречка с жареными шампиньонами и луком",
            "category": DishCategory.SIDE_DISH,
            "allergens": []
        },
        {
            "name": "Рис отварной",
            "description": "Рассчытчатый рис-гарнир",
            "category": DishCategory.SIDE_DISH,
            "allergens": []
        },
        {
            "name": "Картошка фри",
            "description": "Хрустящий картофель, обжаренный во фритюре",
            "category": DishCategory.SIDE_DISH,
            "allergens": []
        },
        {
            "name": "Овощи гриль",
            "description": "Кабачки, баклажаны, перцы на гриле",
            "category": DishCategory.SIDE_DISH,
            "allergens": []
        },
        {
            "name": "Паста (спагетти)",
            "description": "Отварные спагетти, можно как гарнир",
            "category": DishCategory.SIDE_DISH,
            "allergens": ["gluten"]
        },
        {
            "name": "Картофель по-деревенски",
            "description": "Запеченный картофель с чесноком и розмарином",
            "category": DishCategory.SIDE_DISH,
            "allergens": []
        },
        {
            "name": "Тушеная капуста",
            "description": "Квашеная капуста, тушеная с луком и томатом",
            "category": DishCategory.SIDE_DISH,
            "allergens": []
        },
        {
            "name": "Картофельные дольки",
            "description": "Запеченные дольки картофеля с пряностями",
            "category": DishCategory.SIDE_DISH,
            "allergens": []
        },
        {
            "name": "Кускус с овощами",
            "description": "Североафриканская крупа с тушеными овощами",
            "category": DishCategory.SIDE_DISH,
            "allergens": ["gluten"]
        },
        {
            "name": "Булгур",
            "description": "Пшеничная крупа с добавлением специй",
            "category": DishCategory.SIDE_DISH,
            "allergens": ["gluten"]
        },
        
        # САЛАТЫ
        {
            "name": "Салат Оливье",
            "description": "Классический салат с мясом, картофелем, яйцами и горошком",
            "category": DishCategory.SALAD,
            "allergens": ["eggs", "dairy"]
        },
        {
            "name": "Сельдь под шубой",
            "description": "Слоеный салат с сельдью, овощами и майонезом",
            "category": DishCategory.SALAD,
            "allergens": ["fish", "eggs", "dairy"]
        },
        {
            "name": "Винегрет",
            "description": "Салат из свеклы, картофеля, моркови и квашеной капусты",
            "category": DishCategory.SALAD,
            "allergens": []
        },
        {
            "name": "Цезарь с креветками",
            "description": "Салат с креветками, пармезаном и соусом",
            "category": DishCategory.SALAD,
            "allergens": ["dairy", "gluten", "eggs", "fish"]
        },
        {
            "name": "Теплый салат с курицей",
            "description": "Теплый салат с куриным филе и овощами",
            "category": DishCategory.SALAD,
            "allergens": []
        },
        {
            "name": "Салат с тунцом",
            "description": "Консервированный тунец с яйцом и оливками",
            "category": DishCategory.SALAD,
            "allergens": ["fish", "eggs"]
        },
        {
            "name": "Мимоза",
            "description": "Слоеный салат с рыбными консервами",
            "category": DishCategory.SALAD,
            "allergens": ["fish", "eggs", "dairy"]
        },
        {
            "name": "Греческий салат",
            "description": "Классика с фетой, огурцами и оливками",
            "category": DishCategory.SALAD,
            "allergens": ["dairy"]
        },
        {
            "name": "Корейская морковь",
            "description": "Острая морковь по-корейски",
            "category": DishCategory.SALAD,
            "allergens": []
        },
        {
            "name": "Салат с авокадо",
            "description": "Микс салата с авокадо и помидорами черри",
            "category": DishCategory.SALAD,
            "allergens": []
        },
        
        # ОСНОВНЫЕ БЛЮДА
        {
            "name": "Паста Карбонара",
            "description": "Спагетти с беконом в сливочном соусе",
            "category": DishCategory.MAIN,
            "allergens": ["dairy", "gluten", "eggs"]
        },
        {
            "name": "Ризотто с грибами",
            "description": "Итальянское ризотто с лесными грибами и пармезаном",
            "category": DishCategory.MAIN,
            "allergens": ["dairy", "celery"]
        },
        {
            "name": "Куриное филе в сливочном соусе",
            "description": "Нежное куриное филе с шампиньонами",
            "category": DishCategory.MAIN,
            "allergens": ["dairy"]
        },
        {
            "name": "Лосось на гриле",
            "description": "Филе лосося с лимоном и зеленью",
            "category": DishCategory.FISH,
            "allergens": ["fish"]
        },
        {
            "name": "Цезарь с курицей",
            "description": "Салат с курицей, пармезаном, сухариками и соусом Цезарь",
            "category": DishCategory.SALAD,
            "allergens": ["dairy", "gluten", "eggs", "fish"]
        },
        {
            "name": "Блины с икрой",
            "description": "Тонкие блины с красной икрой",
            "category": DishCategory.MAIN,
            "allergens": ["gluten", "eggs", "dairy", "fish"]
        },
        {
            "name": "Картофельное пюре",
            "description": "Нежное пюре со сливками и маслом",
            "category": DishCategory.SIDE_DISH,
            "allergens": ["dairy"]
        },
        {
            "name": "Стейк Рибай",
            "description": "Мраморная говядина с розмарином и чесноком",
            "category": DishCategory.MEAT,
            "allergens": []
        },
        {
            "name": "Тофу в кисло-сладком соусе",
            "description": "Обжаренный тофу с овощами",
            "category": DishCategory.VEGAN,
            "allergens": ["soy", "sesame", "gluten"]
        },
        {
            "name": "Пельмени домашние",
            "description": "Ручная лепка, подаются со сметаной",
            "category": DishCategory.MAIN,
            "allergens": ["gluten", "eggs", "dairy"]
        },
        {
            "name": "Лазанья",
            "description": "Паста с мясом, томатным и сливочным соусом",
            "category": DishCategory.MAIN,
            "allergens": ["dairy", "gluten"]
        },
        {
            "name": "Жульен с курицей",
            "description": "Грибы и курица под сырной корочкой",
            "category": DishCategory.MAIN,
            "allergens": ["dairy"]
        },
        {
            "name": "Овощное рагу",
            "description": "Тушеные овощи с пряными травами",
            "category": DishCategory.VEGAN,
            "allergens": []
        },
        {
            "name": "Котлеты по-киевски",
            "description": "Куриные котлеты с маслом внутри",
            "category": DishCategory.MEAT,
            "allergens": ["eggs", "gluten"]
        },
        
        # ПИЦЦА
        {
            "name": "Пицца Маргарита",
            "description": "Томатный соус, моцарелла, базилик",
            "category": DishCategory.MAIN,
            "allergens": ["dairy", "gluten"]
        },
        {
            "name": "Пицца Пепперони",
            "description": "Пикантная салями, сыр, томатный соус",
            "category": DishCategory.MAIN,
            "allergens": ["dairy", "gluten"]
        },
        {
            "name": "Пицца Четыре сыра",
            "description": "Моцарелла, горгонзола, пармезан, эмменталь",
            "category": DishCategory.MAIN,
            "allergens": ["dairy", "gluten"]
        },
        {
            "name": "Пицца Гавайская",
            "description": "Ветчина, ананас, сыр",
            "category": DishCategory.MAIN,
            "allergens": ["dairy", "gluten"]
        },
        {
            "name": "Пицца Мясная",
            "description": "Ветчина, пепперони, бекон, говядина",
            "category": DishCategory.MEAT,
            "allergens": ["dairy", "gluten"]
        },
        {
            "name": "Пицца Вегетарианская",
            "description": "Перец, грибы, оливки, лук, помидоры",
            "category": DishCategory.VEGAN,
            "allergens": ["dairy", "gluten"]
        },
        {
            "name": "Пицца с морепродуктами",
            "description": "Креветки, мидии, кальмары, сыр",
            "category": DishCategory.FISH,
            "allergens": ["fish", "dairy", "gluten"]
        },
        {
            "name": "Пицца с трюфелями",
            "description": "Премиальная пицца с трюфельным маслом",
            "category": DishCategory.MAIN,
            "allergens": ["dairy", "gluten"]
        },
        
        # ДЕСЕРТЫ
        {
            "name": "Наполеон",
            "description": "Классический слоеный торт с заварным кремом",
            "category": DishCategory.DESSERT,
            "allergens": ["gluten", "dairy", "eggs"]
        },
        {
            "name": "Тирамису",
            "description": "Итальянский десерт с маскарпоне и кофе",
            "category": DishCategory.DESSERT,
            "allergens": ["dairy", "eggs", "gluten"]
        },
        {
            "name": "Чизкейк Нью-Йорк",
            "description": "Классический сырный десерт",
            "category": DishCategory.DESSERT,
            "allergens": ["dairy", "eggs", "gluten"]
        },
        {
            "name": "Шоколадный брауни",
            "description": "Пирожное с орехами и шоколадной глазурью",
            "category": DishCategory.DESSERT,
            "allergens": ["dairy", "eggs", "gluten", "nuts"]
        },
        {
            "name": "Панна-котта",
            "description": "Итальянский десерт с ягодным соусом",
            "category": DishCategory.DESSERT,
            "allergens": ["dairy"]
        },
        {
            "name": "Яблочный штрудель",
            "description": "Слоеное тесто с яблоками и корицей",
            "category": DishCategory.DESSERT,
            "allergens": ["gluten", "dairy", "nuts"]
        },
        {
            "name": "Мороженое пломбир",
            "description": "Классическое мороженое, 3 шарика",
            "category": DishCategory.DESSERT,
            "allergens": ["dairy"]
        },
        {
            "name": "Эклеры с заварным кремом",
            "description": "Заварные пирожные с ванильным кремом",
            "category": DishCategory.DESSERT,
            "allergens": ["gluten", "eggs", "dairy"]
        },
        {
            "name": "Птичье молоко",
            "description": "Нежное суфле в шоколаде",
            "category": DishCategory.DESSERT,
            "allergens": ["dairy", "eggs"]
        },
        {
            "name": "Медовик",
            "description": "Торт с медовыми коржами и сметанным кремом",
            "category": DishCategory.DESSERT,
            "allergens": ["dairy", "eggs", "gluten"]
        },
        
        # ВЕГАНСКОЕ
        {
            "name": "Боул с киноа",
            "description": "Киноа, авокадо, тофу, овощи",
            "category": DishCategory.VEGAN,
            "allergens": ["soy", "sesame"]
        },
        {
            "name": "Хумус с овощами",
            "description": "Традиционный нутовый паштет с овощными палочками",
            "category": DishCategory.VEGAN,
            "allergens": ["sesame"]
        },
        {
            "name": "Веганские роллы",
            "description": "Роллы с огурцом, авокадо и овощами",
            "category": DishCategory.VEGAN,
            "allergens": ["soy", "sesame", "gluten"]
        },
        {
            "name": "Карри с нутом",
            "description": "Индийское карри с кокосовым молоком",
            "category": DishCategory.VEGAN,
            "allergens": []
        },
        {
            "name": "Рататуй",
            "description": "Тушеные овощи по-французски",
            "category": DishCategory.VEGAN,
            "allergens": []
        },
        {
            "name": "Фалафель",
            "description": "Шарики из нута, подаются с соусом тахини",
            "category": DishCategory.VEGAN,
            "allergens": ["sesame", "gluten"]
        },
        {
            "name": "Веганский смузи боул",
            "description": "Смузи из ягод с гранолой и фруктами",
            "category": DishCategory.VEGAN,
            "allergens": ["nuts"]
        },
        
        # НАПИТКИ — теперь с запятой перед этим блоком!
        {
            "name": "Чай черный",
            "description": "Классический черный чай. Подается с сахаром и лимоном",
            "category": DishCategory.DRINK,
            "allergens": []
        },
        {
            "name": "Чай зеленый",
            "description": "Освежающий зеленый чай с жасмином",
            "category": DishCategory.DRINK,
            "allergens": []
        },
        {
            "name": "Кофе американо",
            "description": "Черный кофе из свежеобжаренных зерен",
            "category": DishCategory.DRINK,
            "allergens": []
        },
        {
            "name": "Кофе капучино",
            "description": "Эспрессо с молочной пеной",
            "category": DishCategory.DRINK,
            "allergens": ["dairy"]
        },
        {
            "name": "Кофе латте",
            "description": "Кофе с большим количеством молока",
            "category": DishCategory.DRINK,
            "allergens": ["dairy"]
        },
        {
            "name": "Морс клюквенный",
            "description": "Домашний морс из свежей клюквы",
            "category": DishCategory.DRINK,
            "allergens": []
        },
        {
            "name": "Компот из сухофруктов",
            "description": "Традиционный компот с курагой, черносливом и изюмом",
            "category": DishCategory.DRINK,
            "allergens": []
        },
        {
            "name": "Лимонад",
            "description": "Домашний лимонад с мятой и лимоном",
            "category": DishCategory.DRINK,
            "allergens": []
        },
        {
            "name": "Сок апельсиновый",
            "description": "Свежевыжатый апельсиновый сок",
            "category": DishCategory.DRINK,
            "allergens": []
        },
        {
            "name": "Квас",
            "description": "Традиционный русский квас",
            "category": DishCategory.DRINK,
            "allergens": ["gluten"]
        }
    ]
    
    print(f"📝 Всего блюд для добавления: {len(dishes_data)}")
    print("=" * 60)
    
    added_count = 0
    existing_count = 0
    
    for d_data in dishes_data:
        dish = db.query(Dish).filter(Dish.name == d_data["name"]).first()
        if not dish:
            dish = Dish(
                name=d_data["name"],
                description=d_data["description"],
                category=d_data["category"]
            )
            db.add(dish)
            db.flush()
            
            for allergen_name in d_data["allergens"]:
                allergen = allergens.get(allergen_name)
                if allergen:
                    db.execute(
                        dish_allergen_association.insert().values(
                            dish_id=dish.id,
                            allergen_id=allergen.id
                        )
                    )
            added_count += 1
            print(f"✅ Добавлено: {d_data['name']} (категория: {d_data['category'].value})")
        else:
            existing_count += 1
            print(f"⏩ Уже есть: {d_data['name']}")
    
    db.commit()
    print("=" * 60)
    print(f"🎉 ГОТОВО! Статистика:")
    print(f"   - Добавлено новых блюд: {added_count}")
    print(f"   - Уже существовало: {existing_count}")
    print("=" * 60)
    
    # Покажем что получилось по категориям
    dishes = db.query(Dish).all()
    print(f"🍽️  Всего блюд в базе: {len(dishes)}")
    print("\n📋 МЕНЮ ПО КАТЕГОРИЯМ:")
    
    from collections import defaultdict
    dishes_by_category = defaultdict(list)
    
    for dish in dishes:
        dishes_by_category[dish.category.value].append(dish)
    
    category_names = {
        "soup": "🥣 СУПЫ",
        "main": "🍲 ОСНОВНЫЕ БЛЮДА",
        "salad": "🥗 САЛАТЫ",
        "dessert": "🍰 ДЕСЕРТЫ",
        "vegan": "🌱 ВЕГАНСКИЕ",
        "meat": "🥩 МЯСНЫЕ",
        "fish": "🐟 РЫБНЫЕ",
        "side_dish": "🍚 ГАРНИРЫ",
        "drink": "🥤 НАПИТКИ",
        "bakery": "🥐 ВЫПЕЧКА"
    }
    
    for category_value, dish_list in dishes_by_category.items():
        category_name = category_names.get(category_value, category_value.upper())
        print(f"\n{category_name}:")
        for dish in dish_list:
            allergen_names = []
            result = db.execute(
                dish_allergen_association.select().where(dish_allergen_association.c.dish_id == dish.id)
            )
            for row in result:
                allergen = db.get(Allergen, row.allergen_id)
                if allergen:
                    allergen_names.append(allergen.name)
            
            allergen_str = f" [⚠️ {', '.join(allergen_names)}]" if allergen_names else " [✅ безопасно]"
            print(f"   • {dish.name}{allergen_str}")

if __name__ == "__main__":
    add_sample_dishes()