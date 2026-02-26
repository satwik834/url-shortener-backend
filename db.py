from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
from config import settings
DB_URL = settings.DATABASE_URL


engine = create_engine(
    DB_URL,
    echo=True,
    future=True,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()