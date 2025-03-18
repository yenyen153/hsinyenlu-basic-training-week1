from sqlalchemy.orm import Session
from app.models import CrawlerLog

def log_to_db(db: Session,log_time:str, message: str):
    log_entry = CrawlerLog(
        time=log_time,
        message=message
    )
    db.add(log_entry)
    db.commit()