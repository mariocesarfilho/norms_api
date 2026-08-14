from sqlalchemy import String, Integer, Column, Text
from app.infra.database import Base

class Norm(Base):
    __tablename__ = 'norms'

    id = Column(Integer, primary_key=True, index=True)
    source_id = Column(Integer, unique=True, nullable=True, index=True)
    act_type = Column(String, nullable=False)
    act_number = Column(Integer, nullable=False)
    agency_unit = Column(String, nullable=False)
    publication = Column(String, nullable=False)
    summary = Column(Text, nullable=False)

