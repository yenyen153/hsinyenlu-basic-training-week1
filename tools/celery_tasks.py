from celery import Celery
from celery.schedules import crontab
import logging
from sqlalchemy.orm import sessionmaker
from tools.crawler_tool import *
from sqlalchemy import create_engine
from app.schemas import *
from crud.post import create_ptt_post, get_post_by_link
from crud.crawler_log import log_to_db
from settings import settings
from datetime import datetime

app = Celery("tasks",
             broker=settings.CELERY_BROKER_URL,
             broker_connection_retry_on_startup=True)

app.conf.beat_schedule = {
    "fetch_ptt_every_hour": {
        "task": "tools.celery_tasks.crawler_update",
        "schedule": crontab(minute=0, hour='*/1')
    }
}
# "schedule": crontab(minute='*/1')

logging.basicConfig(
    filename="crawler.log",
    level=logging.INFO,
    filemode='a',
    format="%(message)s",
    encoding='utf-8'
)

engine = create_engine(settings.DATABASE_URL)
Session = sessionmaker(bind=engine)
PTT_BOARDS = ['C_Chat', 'Lifeismoney', 'home-sale', 'NBA', 'mobilecomm','baseball']


@app.task
def crawler_update():
    db = Session()

    for board in PTT_BOARDS:
        log_message = f"正在爬取 {board}"
        logging.info(log_message)
        log_to_db(db, log_message)

        links = fetch_link(board)
        for link in links:
            try:
                post = fetch_post_detail(link)
                post['board_name'] = board

                try:
                    post['date'] = datetime.strptime(post['date'], "%Y/%m/%d %H:%M:%S")
                except:
                    pass

                existing_post = get_post_by_link(db, post['link'])
                if existing_post:
                    return

                new_post = CreatePosts(**post)
                create_ptt_post(db, **dict(new_post))
                db.commit()

            except ValueError:
                db.rollback()

            except:
                db.rollback()

            finally:
                db.close()
