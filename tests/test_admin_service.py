import pytest
from backend.services.AdminService import AdminService
from backend.models.StudentModel import StudentModel
from werkzeug.security import check_password_hash

def test_add_user_ok(db):
    user = AdminService.add_user(db, username="alice", name="Alice", password="123456")
    assert user.id is not None
    assert user.username == "alice"
    assert check_password_hash(user.password, "123456")

def test_add_user_duplicate(db):
    AdminService.add_user(db, username="bob", name="Bob", password="123456")
    with pytest.raises(Exception, match="用户名已存在"):
        AdminService.add_user(db, username="bob", name="Bob2", password="111")

def test_delete_user_cascade_progress(db):
    from backend.models.ProgressModel import ProgressModel
    from datetime import date

    user = AdminService.add_user(db, "tom", "Tom", "pwd")
    db.add(ProgressModel(student_id=user.id, date=date.today(),
                         work_time=8, effective_time=6, main_work="test"))
    db.flush()
    AdminService.delete_user(db, user.id)
    assert db.query(StudentModel).get(user.id) is None
    assert db.query(ProgressModel).filter_by(student_id=user.id).first() is None

def test_change_password(db):
    user = AdminService.add_user(db, "lucy", "Lucy", "old")
    AdminService.change_password(db, user.id, "new")
    db.refresh(user)
    assert check_password_hash(user.password, "new")