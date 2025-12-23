import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    secret_key: str = os.getenv("SECRET_KEY", "hard-to-guess-secret-key")
    db_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg2://postgres:postgres@localhost:5432/progress"
    )
    smtp_server: str = os.getenv("SMTP_SERVER", "smtp.exmail.qq.com")
    smtp_port: int = int(os.getenv("SMTP_PORT", "465"))
    email_addr: str = os.getenv("EMAIL_ADDRESS", "")
    email_pwd: str = os.getenv("EMAIL_PASSWORD", "")
    recipients_csv: str = os.getenv("RECIPIENTS_CSV", "instance/recipients.csv")

settings = Settings()