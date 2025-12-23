from sqlalchemy.orm import Session
from backend.models.StudentModel import StudentModel

class StudentService:
    @staticmethod
    def list_all(db: Session):
        return db.query(StudentModel).all()