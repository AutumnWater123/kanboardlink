from datetime import date, timedelta
from backend.core.database import SessionLocal
from backend.services.EmailService import EmailService

def run():
    target = date.today() - timedelta(days=1)
    with SessionLocal() as db:
        EmailService.send_daily_report(db, target)

if __name__ == "__main__":
    run()