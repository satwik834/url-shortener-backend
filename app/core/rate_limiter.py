from app.redis import redis_client
from fastapi import HTTPException

RATE_LIMIT = 10
WINDOW_SIZE = 60

def check_rate_limit(user_id: int):
    key = f"rate_limit:{user_id}"
    
    # Use pipeline to fetch count and TTL transactionally
    pipe = redis_client.pipeline()
    pipe.incr(key)
    pipe.ttl(key)
    current_count, ttl = pipe.execute()

    # If key was just created (or is missing TTL for some reason), set expiry
    if current_count == 1 or ttl == -1:
        redis_client.expire(key, WINDOW_SIZE)
    
    if current_count > RATE_LIMIT:
        raise HTTPException(
            status_code=409,
            detail="Rate limit Exceeded"
        )
