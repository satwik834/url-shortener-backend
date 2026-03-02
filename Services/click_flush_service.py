from db import SessionLocal
from redis_client import redis_client
from db_ops import get_link_by_short_url

def flush_clicks_to_db():
    db = SessionLocal()
    try:
        for key in redis_client.scan_iter("clicks:*"):
            short_code = key.split(":")[1]
            count = int(redis_client.get(key) or 0)

            if count == 0:
                continue

            link = get_link_by_short_url(db=db, short_url=short_code)
            if link:
                link.click_count += count

            redis_client.delete(key)

        db.commit()
    finally:
        db.close()