import pytest
from datetime import datetime, timedelta
from jose import jwt
from utils.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    SECRET_KEY,
    ALGORITHM
)

class TestPasswordHashing:
    """Тесты для хэширования паролей"""
    
    def test_hash_password_returns_string(self):
        password = "test123"
        hashed = get_password_hash(password)
        assert isinstance(hashed, str)
        assert len(hashed) > 0
    
    def test_hash_password_different_for_same_password(self):
        password = "test123"
        hash1 = get_password_hash(password)
        hash2 = get_password_hash(password)
        assert hash1 != hash2
    
    def test_verify_password_correct(self):
        password = "test123"
        hashed = get_password_hash(password)
        assert verify_password(password, hashed) is True
    
    def test_verify_password_incorrect(self):
        password = "test123"
        wrong_password = "wrong456"
        hashed = get_password_hash(password)
        assert verify_password(wrong_password, hashed) is False
    
    def test_empty_password(self):
        hashed = get_password_hash("")
        assert verify_password("", hashed) is True
        assert verify_password("x", hashed) is False
    
    def test_long_password(self):
        long_password = "a" * 100
        hashed = get_password_hash(long_password)
        assert verify_password(long_password, hashed) is True


class TestAccessToken:
    """Тесты для Access Token"""
    
    def test_create_access_token_returns_string(self):
        token = create_access_token(data={"sub": "1"})
        assert isinstance(token, str)
        assert len(token) > 0
    
    def test_access_token_has_correct_subject(self):
        user_id = "42"
        token = create_access_token(data={"sub": user_id})
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        assert payload["sub"] == user_id
    
    def test_access_token_has_expiration(self):
        token = create_access_token(data={"sub": "1"})
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        assert "exp" in payload
    
    def test_access_token_has_expiration_timestamp(self):
        token = create_access_token(data={"sub": "1"})
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        exp = payload["exp"]
        assert isinstance(exp, int)
        assert exp > 0
    
    def test_refresh_token_has_longer_expiration(self):
        access_token = create_access_token(data={"sub": "1"})
        refresh_token = create_refresh_token(data={"sub": "1"})
        access_payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        refresh_payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        assert refresh_payload["exp"] > access_payload["exp"]


class TestRefreshToken:
    """Тесты для Refresh Token"""
    
    def test_create_refresh_token_returns_string(self):
        token = create_refresh_token(data={"sub": "1"})
        assert isinstance(token, str)
        assert len(token) > 0
    
    def test_refresh_token_has_type_refresh(self):
        token = create_refresh_token(data={"sub": "1"})
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        assert payload["type"] == "refresh"
    
    def test_refresh_token_has_correct_subject(self):
        user_id = "42"
        token = create_refresh_token(data={"sub": user_id})
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        assert payload["sub"] == user_id


class TestTokenEdgeCases:
    """Тесты граничных случаев для токенов"""
    
    def test_token_with_empty_data(self):
        token = create_access_token(data={})
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        assert "exp" in payload
    
    def test_token_with_special_characters_in_sub(self):
        special_sub = "user@123#"
        token = create_access_token(data={"sub": special_sub})
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        assert payload["sub"] == special_sub
    
    def test_token_verification_with_wrong_secret_fails(self):
        token = create_access_token(data={"sub": "1"})
        with pytest.raises(jwt.JWTError):
            jwt.decode(token, "wrong_secret", algorithms=[ALGORITHM])
    
    def test_expired_token_fails(self):
        expired_delta = timedelta(seconds=-1)
        token = create_access_token(data={"sub": "1"}, expires_delta=expired_delta)
        with pytest.raises(jwt.ExpiredSignatureError):
            jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    def test_token_with_extra_data(self):
        token = create_access_token(data={"sub": "1", "custom_field": "custom_value"})
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        assert payload["custom_field"] == "custom_value"