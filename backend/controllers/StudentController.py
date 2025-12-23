from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.core.database import get_db
from backend.services.StudentService import StudentService
from pydantic import BaseModel

router = APIRouter()

class StuOut(BaseModel):
    id: int
    name: str
    username: str

@router.get("/students", response_model=list[StuOut])
def list_students(db: Session = Depends(get_db)):
    return StudentService.list_all(db)