from typing import List
from models.dish import Dish

def recommend_dishes(user_allergens: List[str], dishes: List[Dish], top_n: int = 5) -> List[Dish]:
    """
    Возвращает блюда, безопасные для пользователя (без аллергенов)
    Можно здесь позже подключить ML-рекомендации
    """
    safe_dishes = [d for d in dishes if not any(a in user_allergens for a in d.allergens)]
    return safe_dishes[:top_n]
