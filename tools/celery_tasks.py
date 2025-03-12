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


app = Celery("task",
             broker=settings.CELERY_BROKER_URL,
             broker_connection_retry_on_startup=True)

app.conf.beat_schedule = {
    "fetch_ptt_every_min": {
        "task": "tools.celery_tasks.crawler_past",
        "schedule": crontab(minute=0, hour='*/1')
    }
}

my_logger = logging.getLogger()

logging.basicConfig(
    filename="crawler.log",
    level=logging.INFO,
    filemode='a',
    format="%(asctime)s %(message)s",
    encoding='utf-8'
)

engine = create_engine(settings.DATABASE_URL)
Session = sessionmaker(bind=engine)


@app.task
def crawler_past():
    PTT_BOARDS = ['C_Chat','Baseball','Lifeismoney','home-sale',"NBA",'mobilecomm']
    db = Session()

    for board in PTT_BOARDS:
        log_message = f"正在爬取 {board}"
        my_logger.info(log_message)
        log_to_db(db, log_message)

        links = fetch_link(board)
        for link in links:
            try:
                post = fetch_author(link)
                post['date'] = datetime.strptime(post['date'], "%Y/%m/%d %H:%M:%S")
                post['board_name'] = board
                new_post = CreatePosts(**post) # todo 可以把這個結果存在變數裡面 (finish)
                create_ptt_post(db, **dict(new_post))
                db.commit() # todo 重複爬問題 須停止

            except ValueError:
                db.rollback()

            finally:
                db.close()
