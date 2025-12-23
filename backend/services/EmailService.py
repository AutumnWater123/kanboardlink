import csv
import os
import smtplib
import ssl
from datetime import date
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from sqlalchemy.orm import Session
from backend.core.config import settings
from backend.models.ProgressModel import ProgressModel
from backend.models.StudentModel import StudentModel

class EmailService:
    @staticmethod
    def load_recipients():
        path = settings.recipients_csv
        if not os.path.exists(path):
            return []
        with open(path, newline="", encoding="utf-8") as f:
            rows = list(csv.reader(f))
        return [r[0].strip() for r in rows if r and r[0].strip()]

    @staticmethod
    def get_color(work_time: int, effective_time: int) -> str:
        if work_time is None or effective_time is None:
            return "lightgrey"
        if work_time >= 8 and effective_time >= 8:
            return "green"
        if work_time >= 8 and effective_time >= 5:
            return "lightgreen"
        if work_time >= 8 and effective_time >= 3:
            return "yellow"
        if work_time >= 4 and effective_time >= 2:
            return "#ffcccc"
        return "red"

    @staticmethod
    def send_daily_report(db: Session, target_date: date):
        recipients = EmailService.load_recipients()
        if not recipients:
            print("⚠️ 无收件人")
            return
        rows = (
            db.query(
                StudentModel.name,
                StudentModel.username,
                ProgressModel.work_time,
                ProgressModel.effective_time,
                ProgressModel.main_work,
                ProgressModel.difficulty,
            )
            .join(ProgressModel, ProgressModel.student_id == StudentModel.id)
            .filter(ProgressModel.date == target_date)
            .all()
        )
        color_count = {
            "green": 0,
            "lightgreen": 0,
            "yellow": 0,
            "#ffcccc": 0,
            "red": 0,
            "lightgrey": 0,
        }
        body = f"<h2>📅 {target_date} 学习进度日报</h2><p>共 {len(rows)} 人提交。</p>"
        if not rows:
            body += "<p>⚠️ 昨日无数据。</p>"
        else:
            lis = ""
            for r in rows:
                color = EmailService.get_color(r.work_time, r.effective_time)
                color_count[color] += 1
                lis += f"""
                <li style='background-color:{color};'>
                    <strong>{r.name} ({r.username})</strong><br>
                    工作时长: {r.effective_time or 0} / {r.work_time or 0} 小时<br>
                    主要工作: {r.main_work or '无'}<br>
                    困难: {r.difficulty or '无'}<br>
                </li><br>
                """
            body += "<h3>📊 颜色分布</h3><ul>"
            for c, n in color_count.items():
                if n:
                    body += f"<li><span style='color:{c};'>{c}</span>: {n} 人</li>"
            body += "</ul><h3>👥 详情</h3><ul>" + lis + "</ul>"
        body += "<p><em>—— 自动化日报系统</em></p>"

        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"📊 {target_date} 学习进度报告"
        msg["From"] = settings.email_addr
        msg["To"] = ", ".join(recipients)
        msg.attach(MIMEText(body, "html", "utf-8"))

        try:
            if settings.smtp_port == 465:
                ctx = ssl.create_default_context()
                with smtplib.SMTP_SSL(settings.smtp_server, 465, context=ctx) as s:
                    s.login(settings.email_addr, settings.email_pwd)
                    s.sendmail(settings.email_addr, recipients, msg.as_string())
            else:
                with smtplib.SMTP(settings.smtp_server, settings.smtp_port) as s:
                    s.starttls()
                    s.login(settings.email_addr, settings.email_pwd)
                    s.sendmail(settings.email_addr, recipients, msg.as_string())
            print(f"✅ 日报已发送至 {len(recipients)} 人")
        except Exception as e:
            print(f"❌ 邮件发送失败: {e}")