from datetime import date
from sqlalchemy.orm import Session
from backend.models.ProgressModel import ProgressModel
from fastapi import HTTPException

class ProgressService:
    @staticmethod
    def get_all_progress(db: Session):
        return db.query(ProgressModel).all()

    @staticmethod
    def get_by_date(db: Session, student_id: int, target_date: date):
        p = (
            db.query(ProgressModel)
            .filter_by(student_id=student_id, date=target_date)
            .first()
        )
        if not p:
            raise HTTPException(404, "No data")
        return p

    @staticmethod
    def submit_today(
        db: Session,
        student_id: int,
        work_time: int,
        effective_time: int,
        main_work: str,
        difficulty: str,
    ):
        today = date.today()
        p = (
            db.query(ProgressModel)
            .filter_by(student_id=student_id, date=today)
            .first()
        )
        if p:
            p.work_time = work_time
            p.effective_time = effective_time
            p.main_work = main_work
            p.difficulty = difficulty
            msg = "更新成功"
        else:
            p = ProgressModel(
                student_id=student_id,
                date=today,
                work_time=work_time,
                effective_time=effective_time,
                main_work=main_work,
                difficulty=difficulty,
            )
            db.add(p)
            msg = "提交成功"
        db.commit()
        db.refresh(p)
        return p, msg