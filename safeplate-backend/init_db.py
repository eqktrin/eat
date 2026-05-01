# init_db.py
from database import engine
from models.user import User, RefreshToken 
from models.dish import Dish
from models.order import Order
from models.favorite import Favorite
from models.allergen import Allergen, dish_allergen_association, user_allergen_association
User.metadata.create_all(bind=engine)
Dish.metadata.create_all(bind=engine)
Order.metadata.create_all(bind=engine)
Favorite.metadata.create_all(bind=engine)
Allergen.metadata.create_all(bind=engine)

RefreshToken.metadata.create_all(bind=engine)
dish_allergen_association.create(bind=engine, checkfirst=True)
user_allergen_association.create(bind=engine, checkfirst=True)