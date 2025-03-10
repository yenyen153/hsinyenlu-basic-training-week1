from celery import Celery
from celery.schedules import crontab
import logging
from sqlalchemy.orm import sessionmaker
from tools.crawler_tool import *
from sqlalchemy import create_engine
from app.schemas import *
from crud.post import data_in
from crud.crawler_log import log_in



app = Celery("task",
             broker="redis://localhost:6379/0",
             broker_connection_retry_on_startup=True)

app.conf.beat_schedule = {
    "fetch_ptt_every_min": {
        "task": "celery_tasks.test_crawler",
        "schedule": crontab(minute='*/1')
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

engine = create_engine("mysql+pymysql://user:password@localhost/ptt_db")
Session = sessionmaker(bind=engine)

@app.task
def run_crawler():
    PTT_BOARDS = ['mobilecomm','C_Chat','Baseball','Lifeismoney','home-sale',"NBA"]
    for board in PTT_BOARDS:
        my_logger.info(f"正在爬取{board}")

    for board in PTT_BOARDS:
        links = fetch_link(board)
        for link in links:
            db = Session()
            try:
                post = fetch_author(link)
                post['date'] = datetime.strptime(post['date'], "%Y/%m/%d %H:%M:%S")

                CreatePosts(**post)
                data_in(db,**post)
                db.commit()
            except Exception as e:
                db.rollback()
                my_logger.error(f"插入失敗: {str(e)}")

            fianlly:
            db.close()


    log_in(Session,'crawler.log')