from fastapi import APIRouter, Depends, Form, Response, Cookie
from sqlalchemy.orm import Session
from backend.core.database import get_db
from backend.services.LoginService import LoginService
from pydantic import BaseModel

router = APIRouter()

class LoginOut(BaseModel):
    success: bool
    student: dict

@router.post("/login", response_model=LoginOut)
def login(
    response: Response,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    stu = LoginService.authenticate(db, username, password)
    response.set_cookie(key="student_id", value=str(stu.id), httponly=True)
    return {"success": True, "student": {"id": stu.id, "name": stu.name, "username": stu.username}}

@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("student_id")
    return {"success": True}

@router.get("/session")
def session(student_id: int | None = Cookie(default=None)):
    if student_id:
        return {"logged_in": True, "student": {"id": student_id}}
    return {"logged_in": False}