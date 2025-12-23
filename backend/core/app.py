from fastapi import FastAPI
from backend.core.database import engine, Base
from backend.controllers import (
    AdminController,
    LoginController,
    ProgressController,
    StudentController,
)

def create_app() -> FastAPI:
    app = FastAPI(title="进度管理", version="1.0")
    Base.metadata.create_all(bind=engine)
    app.include_router(AdminController.router, prefix="/admin", tags=["后台"])
    app.include_router(LoginController.router, prefix="/api", tags=["登录"])
    app.include_router(StudentController.router, prefix="/api", tags=["学生"])
    app.include_router(ProgressController.router, prefix="/api", tags=["进展"])
    return app