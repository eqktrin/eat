from fastapi import APIRouter, Depends, HTTPException, status, Form, Body, Response
from sqlalchemy.orm import Session
from database import get_db
from models import User
from models.user import RefreshToken
from models.user import UserRole
from schemas.auth import UserCreate, UserLogin, UserResponse
from utils.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    create_refresh_token,
    REFRESH_TOKEN_EXPIRE_DAYS
)
from dependencies import get_current_user, get_current_admin_user
from datetime import datetime, timedelta
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    logger.info(f"Register attempt with email: {user.email}")
    
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        logger.warning(f"Email already registered: {user.email}")
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(user.password)
    new_user = User(
        email=user.email,
        password_hash=hashed_password,
        role=UserRole.USER
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    logger.info(f"User registered successfully: {user.email}")
    return new_user


@router.post("/login")
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    logger.info(f"Login attempt with email: {user_data.email}")
    
    user = db.query(User).filter(User.email == user_data.email).first()
    if not user or not verify_password(user_data.password, user.password_hash):
        logger.warning(f"Failed login for email: {user_data.email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})
    
    expires_at = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    db_refresh = RefreshToken(
        token=refresh_token,
        user_id=user.id,
        expires_at=expires_at
    )
    db.add(db_refresh)
    db.commit()
    
    response = Response(
        content=json.dumps({
            "access_token": access_token,
            "token_type": "bearer"
        }),
        media_type="application/json"
    )
    
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
    )
    
    logger.info(f"Successful login for email: {user_data.email}")
    return response


@router.post("/token")
async def token_login(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    logger.info(f"Token login attempt with username: {username}")
    
    user = db.query(User).filter(User.email == username).first()
    
    if not user or not verify_password(password, user.password_hash):
        logger.warning(f"Failed token login for username: {username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})
    
    expires_at = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    db_refresh = RefreshToken(
        token=refresh_token,
        user_id=user.id,
        expires_at=expires_at
    )
    db.add(db_refresh)
    db.commit()
    
    response = Response(
        content=json.dumps({
            "access_token": access_token,
            "token_type": "bearer"
        }),
        media_type="application/json"
    )
    
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
    )
    
    logger.info(f"Successful token login for username: {username}")
    return response


@router.post("/refresh")
def refresh_token(
    refresh_token: str = Body(..., embed=True),
    db: Session = Depends(get_db)
):
    logger.info("Attempt to refresh access token")
    
    db_refresh = db.query(RefreshToken).filter(
        RefreshToken.token == refresh_token,
        RefreshToken.expires_at > datetime.utcnow()
    ).first()
    
    if not db_refresh:
        logger.warning("Invalid or expired refresh token")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token"
        )
    
    new_access_token = create_access_token(data={"sub": str(db_refresh.user_id)})
    
    logger.info(f"Access token refreshed for user {db_refresh.user_id}")
    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }


@router.post("/logout")
def logout(
    refresh_token: str = Body(..., embed=True),
    db: Session = Depends(get_db)
):
    logger.info("Logout attempt")
    
    deleted = db.query(RefreshToken).filter(
        RefreshToken.token == refresh_token
    ).delete()
    db.commit()
    
    response = Response(
        content=json.dumps({"message": "Logged out successfully"}),
        media_type="application/json"
    )
    response.delete_cookie("refresh_token")
    
    if deleted:
        logger.info("Logged out successfully")
        return response
    else:
        logger.warning("Refresh token not found")
        return {"message": "Already logged out"}


@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/admin-only")
def admin_endpoint(current_user: User = Depends(get_current_admin_user)):
    return {"message": f"Hello admin {current_user.email}"}


@router.post("/make-admin/{user_id}")
def make_admin(
    user_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.role = UserRole.ADMIN
    db.commit()
    
    return {"message": f"User {user.email} is now admin"}