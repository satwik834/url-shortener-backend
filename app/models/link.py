from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
import datetime
from app.models.base import Base

class Link(Base):
    __tablename__ = "links"

    link_id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=lambda: datetime.datetime.now(datetime.UTC))    
    long_url = Column(String, nullable=False)
    short_url = Column(String, unique=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False, index=True)
    click_count = Column(Integer, default=0)

    user = relationship("User", back_populates="links")
