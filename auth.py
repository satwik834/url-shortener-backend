from datetime import timedelta
import datetime
from jose import JWTError,jwt
from fastapi import HTTPException, status,Depends
from fastapi.security import OAuth2PasswordBearer
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from sqlalchemy.orm import Session
from db import get_db
from db_ops import get_user_by_id

SECRET_KEY = "THIS_IS_A_SECRET"
ALGO = "HS256"
ACCESS_TOKEN_EXPIRE = 60
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

ph = PasswordHasher()
def hash_password(password:str):
    return ph.hash(password)

def verify_password(plain_password:str,hashed_password:str):
    try:
        ph.verify(hashed_password,plain_password)
        return True
    except VerifyMismatchError:
        return False

def create_access_token(user_id:int):
    expire = datetime.datetime.now(datetime.UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE)
    payload = {
        "sub":str(user_id),
        "exp":expire
    }
    return jwt.encode(payload,SECRET_KEY,algorithm=ALGO)

def verify_token(token:str):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGO])
        user_id: str = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="invalid token"
            )
        return int(user_id)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

def get_current_user(
        token:str = Depends(oauth2_scheme),
        db:Session = Depends(get_db)
):
    user_id = verify_token(token)
    user = get_user_by_id(db,user_id)

    if not user:
        raise HTTPException(status_code=401,detail="User not found")
    
    return user