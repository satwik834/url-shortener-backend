from pydantic import BaseModel, HttpUrl
from datetime import datetime

class URLRequest(BaseModel):
    long_url: HttpUrl

class LinkResponse(BaseModel):
    link_id: int
    short_url: str
    long_url: str
    created_at: datetime
    click_count: int

    class Config:
        from_attributes = True
