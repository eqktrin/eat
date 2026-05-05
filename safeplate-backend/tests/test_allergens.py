import pytest
from fastapi.testclient import TestClient
from main import app
from database import SessionLocal, Base, engine
from models.user import User, UserRole
from models.allergen import Allergen, user_allergen_association
from utils.security import get_password_hash, create_access_token
from sqlalchemy import select

client = TestClient(app)


# ========== НАСТРОЙКА БД ДЛЯ ТЕСТОВ ==========
@pytest.fixture(autouse=True, scope="function")
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def test_user(db):
    user = User(
        email="test@example.com",
        password_hash=get_password_hash("secret123"),
        role=UserRole.USER
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def test_user_token(test_user):
    return create_access_token(data={"sub": str(test_user.id)})


# ========== ТЕСТЫ ==========

class TestGetKnownAllergens:
    """GET /allergens/"""
    
    def test_get_known_allergens_returns_list(self):
        response = client.get("/allergens/")
        assert response.status_code == 200
        data = response.json()
        assert "allergens" in data
        assert isinstance(data["allergens"], list)
        assert len(data["allergens"]) > 0
        assert "dairy" in data["allergens"]
        assert "nuts" in data["allergens"]


class TestGetMyAllergens:
    """GET /allergens/my"""
    
    def test_get_my_allergens_without_token_returns_401(self):
        response = client.get("/allergens/my")
        assert response.status_code == 401
    
    def test_get_my_allergens_with_empty_allergens(self, test_user_token):
        response = client.get(
            "/allergens/my",
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "user_id" in data
        assert "allergens" in data
        assert data["allergens"] == []
    
    def test_get_my_allergens_with_existing_allergens(self, test_user_token, test_user, db):
        # Добавляем аллерген пользователю
        allergen = Allergen(name="dairy")
        db.add(allergen)
        db.flush()
        db.execute(
            user_allergen_association.insert().values(
                user_id=test_user.id,
                allergen_id=allergen.id
            )
        )
        db.commit()
        
        response = client.get(
            "/allergens/my",
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["user_id"] == test_user.id
        assert "dairy" in data["allergens"]


class TestUpdateMyAllergens:
    """POST /allergens/update"""
    
    def test_update_allergens_without_token_returns_401(self):
        response = client.post("/allergens/update", json={"allergens": ["nuts"]})
        assert response.status_code == 401
    
    def test_update_allergens_creates_new_allergens(self, test_user_token, test_user, db):
        response = client.post(
            "/allergens/update",
            json={"allergens": ["nuts", "dairy"]},
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Allergens updated"
        assert data["user_id"] == test_user.id
        assert set(data["allergens"]) == {"nuts", "dairy"}
        
        result = db.execute(
            select(Allergen.name)
            .select_from(user_allergen_association)
            .join(Allergen, Allergen.id == user_allergen_association.c.allergen_id)
            .where(user_allergen_association.c.user_id == test_user.id)
        )
        saved_allergens = [row[0] for row in result]
        assert set(saved_allergens) == {"nuts", "dairy"}
    
    def test_update_allergens_replaces_old_allergens(self, test_user_token, test_user, db):
        client.post(
            "/allergens/update",
            json={"allergens": ["nuts", "dairy"]},
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        
        response2 = client.post(
            "/allergens/update",
            json={"allergens": ["gluten", "eggs"]},
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        assert response2.status_code == 200
        data = response2.json()
        assert set(data["allergens"]) == {"gluten", "eggs"}
        
        result = db.execute(
            select(Allergen.name)
            .select_from(user_allergen_association)
            .join(Allergen, Allergen.id == user_allergen_association.c.allergen_id)
            .where(user_allergen_association.c.user_id == test_user.id)
        )
        saved_allergens = [row[0] for row in result]
        assert "nuts" not in saved_allergens
        assert "dairy" not in saved_allergens
        assert "gluten" in saved_allergens
        assert "eggs" in saved_allergens
    
    def test_update_allergens_with_empty_list_removes_all(self, test_user_token, test_user, db):
        client.post(
            "/allergens/update",
            json={"allergens": ["nuts", "dairy"]},
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        
        response = client.post(
            "/allergens/update",
            json={"allergens": []},
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["allergens"] == []
        
        result = db.execute(
            select(Allergen.name)
            .select_from(user_allergen_association)
            .join(Allergen, Allergen.id == user_allergen_association.c.allergen_id)
            .where(user_allergen_association.c.user_id == test_user.id)
        )
        saved_allergens = [row[0] for row in result]
        assert saved_allergens == []
    
    def test_update_allergens_creates_new_allergen_if_not_exists(self, test_user_token, db):
        response = client.post(
            "/allergens/update",
            json={"allergens": ["unknown_allergen_12345"]},
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "unknown_allergen_12345" in data["allergens"]
        
        allergen_in_db = db.query(Allergen).filter(Allergen.name == "unknown_allergen_12345").first()
        assert allergen_in_db is not None
    
    def test_update_allergens_with_duplicates_handles_gracefully(self, test_user_token):
        response = client.post(
            "/allergens/update",
            json={"allergens": ["nuts", "nuts", "dairy", "nuts"]},
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["allergens"]) == 2
        assert "nuts" in data["allergens"]
        assert "dairy" in data["allergens"]


class TestAllergensEdgeCases:
    """Граничные случаи"""
    
    def test_multiple_users_have_isolated_allergens(self, db):
        # Создаём двух пользователей
        user1 = User(
            email="user1@example.com",
            password_hash=get_password_hash("pass123"),
            role=UserRole.USER
        )
        user2 = User(
            email="user2@example.com",
            password_hash=get_password_hash("pass123"),
            role=UserRole.USER
        )
        db.add_all([user1, user2])
        db.commit()
        db.refresh(user1)
        db.refresh(user2)
        
        token1 = create_access_token(data={"sub": str(user1.id)})
        token2 = create_access_token(data={"sub": str(user2.id)})
        
        # User1 добавляет аллергены
        client.post(
            "/allergens/update",
            json={"allergens": ["nuts", "dairy"]},
            headers={"Authorization": f"Bearer {token1}"}
        )
        
        # User2 добавляет другие
        client.post(
            "/allergens/update",
            json={"allergens": ["gluten"]},
            headers={"Authorization": f"Bearer {token2}"}
        )
        
        # Проверяем User1
        resp1 = client.get("/allergens/my", headers={"Authorization": f"Bearer {token1}"})
        assert set(resp1.json()["allergens"]) == {"nuts", "dairy"}
        
        # Проверяем User2
        resp2 = client.get("/allergens/my", headers={"Authorization": f"Bearer {token2}"})
        assert resp2.json()["allergens"] == ["gluten"]