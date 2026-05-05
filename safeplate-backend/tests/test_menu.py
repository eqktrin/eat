import pytest
from fastapi.testclient import TestClient
import main
from models.user import UserRole

client = TestClient(main.app)


def test_get_menu_public(client, user_token):
    response = client.get(
        "/menu/",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 200


def test_get_dish_by_id(client, user_token, sample_dish):
    response = client.get(
        f"/menu/{sample_dish.id}",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == sample_dish.name


def test_admin_can_create_dish(client, admin_token, admin_user):
    # Проверяем, что пользователь действительно админ
    assert admin_user.role == UserRole.ADMIN
    
    response = client.post(
        "/menu/",
        json={
            "name": "New Dish From Test",
            "description": "Tasty",
            "category": "main",
            "allergens": []
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    # Если 403 — выведем информацию для отладки
    if response.status_code == 403:
        print(f"\n🔍 Token user ID: {admin_token.split('.')[1]}")
        print(f"🔍 Admin user ID: {admin_user.id}")
        print(f"🔍 Admin user role: {admin_user.role}")
    
    assert response.status_code == 200
    assert response.json()["name"] == "New Dish From Test"