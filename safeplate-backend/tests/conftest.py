import pytest
from fastapi.testclient import TestClient
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

import main
from database import Base, engine, SessionLocal, get_db
from models.user import User, UserRole
from models.dish import Dish
from utils.security import get_password_hash, create_access_token


# ========== БАЗА ДАННЫХ ==========
@pytest.fixture(scope="session", autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def override_get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ========== ОВЕРРАЙД DEPENDENCIES ==========
def override_get_current_user_for_tests():
    """Возвращает тестового пользователя (при наличии токена)"""
    db = SessionLocal()
    user = db.query(User).filter(User.email == "test@example.com").first()
    if not user:
        user = User(
            email="test@example.com",
            password_hash=get_password_hash("secret123"),
            role=UserRole.USER
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    db.close()
    return user


def override_get_current_admin_for_tests():
    db = SessionLocal()
    admin = db.query(User).filter(User.email == "admin@example.com").first()
    if not admin:
        admin = User(
            email="admin@example.com",
            password_hash=get_password_hash("admin123"),
            role=UserRole.ADMIN
        )
        db.add(admin)
        db.commit()
        db.refresh(admin)
    db.close()
    return admin


from dependencies import get_current_user, get_current_admin_user, oauth2_scheme

# Очищаем overrides перед настройкой
main.app.dependency_overrides.clear()
main.app.dependency_overrides[get_db] = override_get_db

# Создаём функцию-обёртку, которая проверяет токен
async def get_current_user_with_override(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(override_get_db)
):
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return override_get_current_user_for_tests()

main.app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
    return TestClient(main.app)


@pytest.fixture
def test_user():
    db = SessionLocal()
    # Очищаем старого пользователя
    db.query(User).filter(User.email == "test@example.com").delete()
    db.commit()
    
    user = User(
        email="test@example.com",
        password_hash=get_password_hash("secret123"),
        role=UserRole.USER
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    return user


@pytest.fixture
def admin_user():
    db = SessionLocal()
    # Очищаем старого админа
    db.query(User).filter(User.email == "admin@example.com").delete()
    db.commit()
    
    admin = User(
        email="admin@example.com",
        password_hash=get_password_hash("admin123"),
        role=UserRole.ADMIN
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    db.close()
    return admin


@pytest.fixture
def user_token(test_user):
    return create_access_token(data={"sub": str(test_user.id)})


@pytest.fixture
def admin_token(admin_user):
    return create_access_token(data={"sub": str(admin_user.id)})


@pytest.fixture
def sample_dish():
    db = SessionLocal()
    dish = db.query(Dish).filter(Dish.name == "Test Dish").first()
    if not dish:
        dish = Dish(
            name="Test Dish",
            description="Test description",
            category="main"
        )
        db.add(dish)
        db.commit()
        db.refresh(dish)
    db.close()
    return dish