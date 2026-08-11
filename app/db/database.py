from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine
from app.core.config import Settings

engine = create_async_engine(Settings.database_url)
Session = sessionmaker(bind=engine)

Base = declarative_base()