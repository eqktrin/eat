# models/__init__.py
from .user import User, UserRole
from .dish import Dish
from .order import Order
from .favorite import Favorite
from .allergen import Allergen, dish_allergen_association, user_allergen_association
from .dish_image import DishImage

__all__ = [
    'User', 
    'UserRole', 
    'Dish', 
    'Order', 
    'Favorite', 
    'Allergen',
    'dish_allergen_association',
    'user_allergen_association'
]