from sqlalchemy import Column, Integer, String
from backend.core.database import Base

class StudentModel(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    username = Column(String(80), unique=True, nullable=False)
    password = Column(String(120), nullable=False)