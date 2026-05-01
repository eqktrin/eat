from typing import List

def check_dish_allergens(dish_allergens: List[str], user_allergens: List[str]):
    """
    Возвращает:
    - dangerous: bool (есть ли пересечение с аллергенами пользователя)
    - conflicts: список аллергенов, которые совпали
    """
    conflicts = [a for a in dish_allergens if a in user_allergens]
    dangerous = len(conflicts) > 0
    return dangerous, conflicts
