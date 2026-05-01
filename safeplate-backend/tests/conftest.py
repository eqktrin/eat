import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base
from main import app
from fastapi.testclient import TestClient
from utils.security import create_access_token, get_password_hash

# Импортируем ВСЕ модели, чтобы SQLAlchemy знал о них
from models.user import User
from models.dish import Dish
from models.order import Order
from models.favorite import Favorite
from models.allergen import Allergen, dish_allergen_association, user_allergen_association
from models.dish_image import DishImage

# Тестовая БД
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(autouse=True)
def setup_database():
    """Создаёт все таблицы перед тестами и удаляет после"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session():
    """Фикстура для сессии БД"""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def admin_token(db_session):
    admin = User(
        email="admin@menu.com",
        password_hash=get_password_hash("admin123"),
        role="ADMIN"
    )
    db_session.add(admin)
    db_session.commit()
    db_session.refresh(admin)
    return create_access_token(data={"sub": str(admin.id)})

@pytest.fixture
def user_token(db_session):
    user = User(
        email="user@menu.com",
        password_hash=get_password_hash("user123"),
        role="USER"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return create_access_token(data={"sub": str(user.id)})

@pytest.fixture
def sample_dish(db_session):
    dish = Dish(
        name="Тестовое блюдо",
        description="Описание тестового блюда",
        category="main"
    )
    db_session.add(dish)
    db_session.commit()
    db_session.refresh(dish)
    return dish

@pytest.fixture
def sample_allergen(db_session):
    allergen = Allergen(name="dairy", description="Молочные продукты")
    db_session.add(allergen)
    db_session.commit()
    db_session.refresh(allergen)
    return allergen