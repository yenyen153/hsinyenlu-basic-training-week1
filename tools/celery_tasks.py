from celery import Celery
from celery.schedules import crontab
import logging
from sqlalchemy.orm import sessionmaker
from tools.crawler_tool import *
from sqlalchemy import create_engine
from app.schemas import *
from crud.post import create_ptt_post
from crud.crawler_log import log_to_db
from settings import settings
from datetime import datetime
from app.models import *
from tools.crawler_past import fetch_board_posts, run_crawler


app = Celery("tasks",
             broker=settings.CELERY_BROKER_URL,
             broker_connection_retry_on_startup=True)

app.conf.beat_schedule = {
    "fetch_ptt_every_hour": {
        "task": "tools.celery_tasks.crawler_update",
        "schedule": crontab(minute=0, hour='*/1')
    }
}

logging.basicConfig(
    filename="crawler.log",
    level=logging.INFO,
    filemode='a',
    format="%(message)s",
    encoding='utf-8'
)

engine = create_engine(settings.DATABASE_URL)
Session = sessionmaker(bind=engine)

@app.task
def crawler_update():
    db = Session()
    ptt_boards = [ "stock","NBA", "Lifeismoney", "home-sale", "mobilecomm","Baseball","c_chat",]
    for board in ptt_boards:
        log_message = f"正在爬取 {board}"
        logging.info(log_message)
        log_to_db(db, log_message)
        try:
            posts = fetch_board_posts(board)
        except Exception as e:
            logging.error(f"Error fetching posts from {board}: {str(e)}")
            continue

        for post in posts:
            db = Session()
            try:
                post['date'] = datetime.strptime(post['date'], "%Y/%m/%d %H:%M:%S")
                CreatePosts(**post)
                create_ptt_post(db, **post)


            except Exception as e:
                logging.error(f"{post['title']}: {str(e)}")
                continue