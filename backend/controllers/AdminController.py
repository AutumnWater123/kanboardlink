from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session
from backend.core.database import get_db
from backend.services.AdminService import AdminService
from pydantic import BaseModel

router = APIRouter()

class UserOut(BaseModel):
    id: int
    name: str
    username: str

@router.get("/users", response_model=list[UserOut])
def list_users(db: Session = Depends(get_db)):
    return AdminService.list_users(db)

@router.post("/users", response_model=UserOut)
def add_user(
    username: str = Form(...),
    name: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    return AdminService.add_user(db, username, name, password)

@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    AdminService.delete_user(db, user_id)
    return {"msg": "已删除"}

@router.post("/users/{user_id}/password")
def change_password(
    user_id: int,
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    AdminService.change_password(db, user_id, password)
    return {"msg": "已更新"}