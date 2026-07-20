from sqlalchemy.orm import Session
from sqlalchemy import text
from app.models.link import Link
from app.utils.helpers import encode_base62

def create_link(db: Session, long_url: str, user_id: int) -> Link:
    """
    Creates a new Link record in a single transaction.
    Uses database sequence to pre-generate the link_id for base62 encoding.
    """
    next_id = db.execute(text("SELECT nextval('links_link_id_seq')")).scalar()
    short_code = encode_base62(next_id)
    
    link = Link(
        link_id=next_id,
        long_url=long_url,
        short_url=short_code,
        user_id=user_id
    )
    db.add(link)
    db.commit()
    db.refresh(link)
    return link

def get_link_by_short_url(db: Session, short_url: str) -> Link | None:
    return db.query(Link).filter(Link.short_url == short_url).first()

def delete_link(db: Session, short_url: str) -> Link | None:
    link = get_link_by_short_url(db, short_url)
    if link:
        db.delete(link)
        db.commit()
    return link

def get_links(db: Session) -> list[Link]:
    return db.query(Link).all()

def get_links_by_user(db: Session, user_id: int) -> list[Link]:
    return db.query(Link).filter(Link.user_id == user_id).all()
