from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
DB_URL = "postgresql+psycopg2://postgres:234856@localhost:5432/urls"


engine = create_engine(
    DB_URL,
    echo=True,
    future=True
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