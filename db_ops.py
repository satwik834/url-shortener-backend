from sqlalchemy.orm import Session
from models import Link,User

def create_link(db:Session,long_url:str,user_id:int):
    link = Link(long_url=long_url,user_id=user_id)
    db.add(link)
    db.commit()
    db.refresh(link)
    return link

def update_short_url(db:Session,link:Link,short_url:str):
    link.short_url = short_url
    db.commit()
    db.refresh(link)
    return link

def get_link_by_short_url(db:Session,short_url:str):
    return db.query(Link).filter(Link.short_url == short_url).first()
    

def delete_link(db:Session,short_url:str):
    link = get_link_by_short_url(db,short_url)
    if link:
        db.delete(link)
        db.commit()
    return link
def get_links(db:Session):
    return db.query(Link).all()

def create_user(db:Session,email:str,hashed:str):
    user = User(
        email=email,
        password_hash = hashed
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user
    
def get_user_by_email(db:Session,email:str):
    return db.query(User).filter(User.email ==  email).first()

def get_user_by_id(db:Session,user_id:int):
    return db.query(User).filter(User.user_id ==  user_id).first()

def get_links_by_user(db:Session,user_id:int):
    return db.query(Link).filter(Link.user_id == user_id).all()
