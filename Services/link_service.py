from sqlalchemy.orm import Session
from db_ops import get_link_by_short_url
from redis_client import redis_client

CACHE_TTL = 3600


def resolve_short_code(short_code:str,db: Session):
    cached_url = redis_client.get(short_code)

    
    if not cached_url:
        link = get_link_by_short_url(db=db,short_url=short_code)
        if not link:
            return None
        cached_url = link.long_url
        redis_client.setex(short_code,CACHE_TTL,cached_url)
    
    redis_client.incr(f"clicks:{short_code}")
    print(redis_client.get("clicks"))

    return cached_url
