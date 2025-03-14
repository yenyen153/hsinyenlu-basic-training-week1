from sqlalchemy.orm import Session
from datetime import datetime
from app.models import CrawlerLog

def log_to_db(db: Session, message: str):
    log_entry = CrawlerLog(
        time=datetime.now(),
        message=message
    )
    db.add(log_entry)
    db.commit()