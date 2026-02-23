from fastapi import FastAPI,Depends,HTTPException
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel,HttpUrl,EmailStr
from datetime import datetime
from helpers import encode_base62
from db_ops import *
from db import get_db
from typing import List
from auth import hash_password,verify_password,create_access_token,get_current_user


app = FastAPI()
origins = [
    "http://localhost:5173",      # React dev server
    "http://127.0.0.1:5173",      # Vite dev server

]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # Allowed origins
    allow_credentials=True,
    allow_methods=["*"],              # Allow all HTTP methods
    allow_headers=["*"],              # Allow all headers
)

class URLRequest(BaseModel):
    long_url: HttpUrl

class LinkResponse(BaseModel):
    link_id: int
    short_url: str
    long_url: str
    created_at: datetime

class UserRequest(BaseModel):
    email: EmailStr
    password: str

@app.get('/')
def root():
    return {"hello":"fast"}

@app.post('/register')
def register(req:UserRequest,db:Session = Depends(get_db)):
    print(req.password)
    
    existing = get_user_by_email(db,req.email)
    if existing:
        raise HTTPException(status_code=400,detail="Email already registered")
    hashed = hash_password(req.password)
    create_user(db,req.email,hashed)

    return {"message":"user created"}
@app.post('/login')
def login(req:UserRequest,db:Session = Depends(get_db)):
    user = get_user_by_email(db,req.email)
    if not user or not verify_password(req.password,user.password_hash):
        raise HTTPException(status_code=400,detail="Invalid credentials")
    
    token = create_access_token(user.user_id)

    return {"access_token":token, "token_type":"bearer"}



@app.post('/shorten')
def shorten(
    request: URLRequest,
    db:Session = Depends(get_db),
    current_user = Depends(get_current_user)
    
):
    try:
        user_id = int(current_user.user_id)
        long_url = str(request.long_url)
        link = create_link(db=db,long_url=long_url,user_id=user_id)

        short_code = encode_base62(link.link_id)

        update_short_url(db=db,link=link,short_url=short_code)

        return {"short_url":short_code}
    except Exception as e:
        raise HTTPException(status_code=500,detail="failed to create short url")
    

@app.get("/links",response_model=List[LinkResponse])
def get_all(
    db:Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    links = get_links_by_user(db=db,user_id =current_user.user_id )

    return links


@app.get('/{short_code}')
def redirect(short_code:str,db:Session=Depends(get_db)):
    link = get_link_by_short_url(db=db,short_url=short_code)
    
    print(short_code,link)
    
    if not link:
        raise HTTPException(status_code=404,detail='Link not found')
    return RedirectResponse(url=link.long_url,status_code=302)
    

@app.delete("/{short_code}")
def delete(
    short_code:str,
    db:Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    link = get_link_by_short_url(short_url=short_code,db=db)

    if not link:
        raise HTTPException(status_code=404,detail='link not found')
    if link.user_id != current_user.user_id:
        raise HTTPException(status_code=403,detail="Not Authorized")
    delete_link(db=db,short_url=short_code)

    return {"message":"deleted"}


@app.post("/test/me")
def me(current_user = Depends(get_current_user)):
    return {
        "user_id": current_user.user_id,
        "email":current_user.email
    }