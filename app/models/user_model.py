from sqlalchemy import String, Integer, Column
from app.infra.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)