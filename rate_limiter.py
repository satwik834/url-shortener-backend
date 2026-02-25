from redis_client import redis_client
from fastapi import HTTPException

RATE_LIMIT = 10
WINDOW_SIZE = 60

def check_rate_limit(user_id:int):
    key = f"rate_limit:{user_id}"
    current_count = redis_client.incr(key)

    if current_count ==1:
        redis_client.expire(key,WINDOW_SIZE)
    
    if current_count > RATE_LIMIT:
        raise HTTPException(
            status_code=409,
            detail="Rate limit Exceeded"
        )