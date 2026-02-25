from redis_client import redis_client
from fastapi import HTTPException

RATE_LIMIT = 10
WINDOW_SIZE = 60

def check_rate_limit():
    return None