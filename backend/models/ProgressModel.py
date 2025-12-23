from sqlalchemy import Column, Integer, Date, Text, ForeignKey, UniqueConstraint
from backend.core.database import Base

class ProgressModel(Base):
    __tablename__ = "progress"

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    date = Column(Date, nullable=False)
    work_time = Column(Integer, nullable=False)
    effective_time = Column(Integer, nullable=False)
    main_work = Column(Text, nullable=True)
    difficulty = Column(Text, nullable=True)

    __table_args__ = (UniqueConstraint("student_id", "date"),)