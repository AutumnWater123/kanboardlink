from datetime import date
from fastapi import APIRouter, Depends, Form, Cookie
from sqlalchemy.orm import Session
from backend.core.database import get_db
from backend.services.ProgressService import ProgressService
from pydantic import BaseModel

router = APIRouter()

class ProgressOut(BaseModel):
    id: int
    student_id: int
    date: date
    work_time: int
    effective_time: int
    main_work: str | None
    difficulty: str | None

@router.get("/progress")
def get_all_progress(db: Session = Depends(get_db)):
    return ProgressService.get_all_progress(db)

@router.get("/progress/{student_id}/{date_str}", response_model=ProgressOut)
def get_by_date(student_id: int, date_str: date, db: Session = Depends(get_db)):
    return ProgressService.get_by_date(db, student_id, date_str)

@router.post("/progress")
def submit(
    work_time: int = Form(...),
    effective_time: int = Form(...),
    main_work: str = Form(""),
    difficulty: str = Form(""),
    db: Session = Depends(get_db),
    student_id: int | None = Cookie(default=None),
):
    if not student_id:
        return {"error": "未登录"}
    p, msg = ProgressService.submit_today(
        db, student_id, work_time, effective_time, main_work, difficulty
    )
    return {"success": True, "message": msg, "progress": p}