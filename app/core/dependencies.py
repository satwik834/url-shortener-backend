from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.security import oauth2_scheme, verify_token
from app.models.user import User
import app.crud.user as crud_user

def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    """
    Optimized dependency that extracts and returns user_id directly from the JWT.
    Bypasses database queries for endpoints that only need user_id.
    """
    return verify_token(token)

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency that retrieves the full User object from the database.
    Used by endpoints that require user fields other than user_id (e.g. email).
    """
    user_id = verify_token(token)
    user = crud_user.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user
