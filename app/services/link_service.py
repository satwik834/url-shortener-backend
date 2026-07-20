from sqlalchemy.orm import Session
from app.redis import redis_client
import app.crud.link as crud_link

CACHE_TTL = 3600
NEGATIVE_CACHE_TTL = 300  # 5 minutes for non-existent links to prevent cache penetration

def resolve_short_code(short_code: str, db: Session) -> str | None:
    """
    Resolves a short code to its original long URL.
    Checks Redis cache first. If it's a miss, queries the database.
    Increments click counts in Redis using HINCRBY.
    """
    cached_url = redis_client.get(short_code)

    if not cached_url:
        link = crud_link.get_link_by_short_url(db=db, short_url=short_code)
        if not link:
            # Cache non-existent codes to prevent database thundering herd / cache penetration
            redis_client.setex(short_code, NEGATIVE_CACHE_TTL, "NULL")
            return None
        
        cached_url = link.long_url
        redis_client.setex(short_code, CACHE_TTL, cached_url)

    if cached_url == "NULL":
        return None

    # Atomically track click counts in Redis
    redis_client.hincrby("clicks_to_flush", short_code, 1)

    return cached_url
