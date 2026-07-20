import uuid
from app.database import SessionLocal
from app.redis import redis_client
import app.crud.link as crud_link

def flush_clicks_to_db():
    """
    Atomically flushes click counts from Redis to PostgreSQL.
    Uses a temporary staging key to prevent concurrency race conditions
    and support multiple worker processes.
    """
    staging_key = f"clicks_flushing:{uuid.uuid4()}"
    
    try:
        # Atomic rename acts as a lock; only one worker succeeds
        redis_client.rename("clicks_to_flush", staging_key)
    except Exception:
        # No clicks key exists, return early
        return

    db = SessionLocal()
    try:
        clicks_data = redis_client.hgetall(staging_key)
        for short_code, count_str in clicks_data.items():
            count = int(count_str)
            if count <= 0:
                continue

            link = crud_link.get_link_by_short_url(db=db, short_url=short_code)
            if link:
                link.click_count += count

        db.commit()
        redis_client.delete(staging_key)
    except Exception as e:
        db.rollback()
        # On database failure, restore counts to redis
        try:
            for short_code, count_str in clicks_data.items():
                redis_client.hincrby("clicks_to_flush", short_code, int(count_str))
            redis_client.delete(staging_key)
        except Exception as redis_err:
            print("Failed to recover clicks to redis:", redis_err)
        raise e
    finally:
        db.close()
