import pytest
from backend.services.LoginService import LoginService
from backend.services.AdminService import AdminService

def test_authenticate_success(db):
    AdminService.add_user(db, "login_ok", "LoginOk", "pwd")
    user = LoginService.authenticate(db, "login_ok", "pwd")
    assert user.username == "login_ok"

def test_authenticate_fail(db):
    AdminService.add_user(db, "login_fail", "LoginFail", "right")
    with pytest.raises(Exception, match="用户名或密码错误"):
        LoginService.authenticate(db, "login_fail", "wrong")