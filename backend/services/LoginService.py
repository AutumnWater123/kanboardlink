from sqlalchemy.orm import Session
from backend.models.StudentModel import StudentModel
from werkzeug.security import check_password_hash
from fastapi import HTTPException

class LoginService:
    @staticmethod
    def authenticate(db: Session, username: str, password: str) -> StudentModel:
        stu = db.query(StudentModel).filter_by(username=username).first()
        if stu and check_password_hash(stu.password, password):
            return stu
        raise HTTPException(401, "用户名或密码错误")