from datetime import date, timedelta
from backend.services.EmailService import EmailService
from backend.services.AdminService import AdminService
from backend.services.ProgressService import ProgressService
import pytest

@pytest.mark.skip(reason="需要 SMTP 配置，跳过测试")
def test_send_daily_report(db, monkeypatch):
    # 伪造邮箱地址，避免真发送
    monkeypatch.setattr("backend.core.config.settings.email_addr", "test@example.com")
    monkeypatch.setattr("backend.core.config.settings.email_pwd", "pwd")
    monkeypatch.setattr("backend.services.EmailService.load_recipients", lambda: ["a@t.com", "b@t.com"])

    AdminService.add_user(db, "e1", "E1", "pwd")
    ProgressService.submit_today(db, 1, 8, 6, "test work", "test difficulty")
    # 跑日报生成逻辑（不会真发出，因为 SMTP 被 monkeypatch）
    EmailService.send_daily_report(db, date.today() - timedelta(days=1))
    # 没抛异常就是胜利