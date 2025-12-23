from sqlalchemy.orm import Session
from backend.models.StudentModel import StudentModel
from werkzeug.security import generate_password_hash
from fastapi import HTTPException

class AdminService:
    @staticmethod
    def list_users(db: Session):
        return db.query(StudentModel).order_by(StudentModel.id).all()

    @staticmethod
    def add_user(db: Session, username: str, name: str, password: str):
        if db.query(StudentModel).filter_by(username=username).first():
            raise HTTPException(400, "用户名已存在")
        stu = StudentModel(
            name=name,
            username=username,
            password=generate_password_hash(password),
        )
        db.add(stu)
        db.commit()
        db.refresh(stu)
        return stu

    @staticmethod
    def delete_user(db: Session, user_id: int):
        stu = db.query(StudentModel).get(user_id)
        if not stu:
            raise HTTPException(404, "用户不存在")
        from backend.models.ProgressModel import ProgressModel
        db.query(ProgressModel).filter_by(student_id=user_id).delete()
        db.delete(stu)
        db.commit()

    @staticmethod
    def change_password(db: Session, user_id: int, new_pwd: str):
        stu = db.query(StudentModel).get(user_id)
        if not stu:
            raise HTTPException(404, "用户不存在")
        stu.password = generate_password_hash(new_pwd)
        db.commit()