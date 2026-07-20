from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import UserRequest
from app.core.security import hash_password, verify_password, create_access_token
from app.core.dependencies import get_current_user
import app.crud.user as crud_user

router = APIRouter()

@router.post('/register')
def register(req: UserRequest, db: Session = Depends(get_db)):
    existing = crud_user.get_user_by_email(db, req.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed = hash_password(req.password)
    crud_user.create_user(db, req.email, hashed)
    return {"message": "user created"}

@router.post('/login')
def login(req: UserRequest, db: Session = Depends(get_db)):
    user = crud_user.get_user_by_email(db, req.email)
    if not user or not verify_password(req.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    token = create_access_token(user.user_id)
    return {"access_token": token, "token_type": "bearer"}

@router.post("/test/me")
def me(current_user = Depends(get_current_user)):
    return {
        "user_id": current_user.user_id,
        "email": current_user.email
    }
