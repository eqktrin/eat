import sys
from database import SessionLocal
from models.user import User
from utils.security import get_password_hash

print(f"Аргументы: {sys.argv}")

def create_admin(email, password):
    db = SessionLocal()
    
    user = db.query(User).filter(User.email == email).first()
    
    if user:
        user.role = "ADMIN"
        user.password_hash = get_password_hash(password) 
        print(f"Пользователь {email} теперь ADMIN (пароль обновлен)")
    else:
        new_admin = User(
            email=email,
            password_hash=get_password_hash(password),
            role="ADMIN"
        )
        db.add(new_admin)
        print(f"Создан новый ADMIN: {email}")
    
    db.commit()
    db.close()

if __name__ == "__main__":
    if len(sys.argv) == 3:
        create_admin(sys.argv[1], sys.argv[2])
    else:
        create_admin("admin@example.com", "admin123")