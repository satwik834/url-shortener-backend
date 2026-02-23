from sqlalchemy import Column, Integer, String, DateTime,ForeignKey
from sqlalchemy.orm import relationship
import datetime
from db import Base

class Link(Base):
    __tablename__ = "links"

    link_id = Column(Integer,primary_key=True,index=False)
    created_at = Column(DateTime, default=lambda: datetime.datetime.now(datetime.UTC))    
    long_url = Column(String,nullable=False)
    short_url = Column(String,unique=True,index=True)
    user_id = Column(Integer,ForeignKey("users.user_id"),nullable=False)
    user = relationship("User",back_populates="links")


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer,primary_key=True)
    email = Column(String,unique=True,nullable=False)
    password_hash = Column(String,nullable=False)

    links = relationship("Link",back_populates="user")