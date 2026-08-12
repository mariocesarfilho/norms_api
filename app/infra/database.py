from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.config import settings

Base = declarative_base()

engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_database():
    with engine.connect() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS authentication"))
        conn.commit()

def create_table():
    Base.metadata.create_all(bind=engine)