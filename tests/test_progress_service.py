import pytest
from datetime import date
from backend.services.ProgressService import ProgressService
from backend.services.AdminService import AdminService
from backend.models.ProgressModel import ProgressModel

def test_submit_new(db):
    AdminService.add_user(db, "u1", "User", "pwd")
    p, msg = ProgressService.submit_today(db, 1, 8, 6, "study", "none")
    assert msg == "提交成功"
    assert p.work_time == 8
    assert p.date == date.today()

def test_submit_duplicate_400(db):
    AdminService.add_user(db, "u2", "User", "pwd")
    ProgressService.submit_today(db, 2, 8, 6, "study", "none")
    with pytest.raises(Exception, match="今日记录已存在"):
        ProgressService.submit_today(db, 2, 8, 6, "study", "none")

def test_get_by_date_exists(db):
    AdminService.add_user(db, "u3", "User", "pwd")
    ProgressService.submit_today(db, 3, 4, 3, "read", "none")
    p = ProgressService.get_by_date(db, 3, date.today())
    assert p.effective_time == 3

def test_get_by_date_missing(db):
    AdminService.add_user(db, "u4", "User", "pwd")
    with pytest.raises(Exception, match="No data"):
        ProgressService.get_by_date(db, 4, date.today())

def test_get_all_progress(db):
    AdminService.add_user(db, "u5", "User", "pwd")
    ProgressService.submit_today(db, 5, 2, 1, "a", "b")
    lst = ProgressService.get_all_progress(db)
    assert len(lst) >= 1