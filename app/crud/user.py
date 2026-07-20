from sqlalchemy.orm import Session
from app.models.user import User

def create_user(db: Session, email: str, hashed: str) -> User:
    user = User(
        email=email,
        password_hash=hashed
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.user_id == user_id).first()
