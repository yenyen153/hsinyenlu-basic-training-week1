from datetime import timedelta
import logging
from sqlalchemy.orm import sessionmaker
from tools.crawler_tool import *
from sqlalchemy import create_engine
from app.schemas import *
from crud.post import create_ptt_post
from settings import settings
from fastapi import status

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

engine = create_engine(settings.DATABASE_URL)
Session = sessionmaker(bind=engine)

def fetch_board_posts(board_name):
    one_year_ago = datetime.now().date() - timedelta(days=365)
    url = f"https://www.ptt.cc/bbs/{board_name}/index.html"
    while url:
        try:
            response = requests.get(url)
        except Exception as e:
            logging.error(e.with_traceback())
            break

        if response.status_code != status.HTTP_200_OK:
            logger.error(f"Failed to fetch {url}, status code: {response.status_code}")
            break

        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.select('div.title a')

        for link in links:
            post_url = 'https://www.ptt.cc' + link['href']
            try:
                post = fetch_post_detail(post_url)
                post_date = datetime.strptime(post['date'], "%Y/%m/%d %H:%M:%S")
                try:
                    if post_date.date() >= one_year_ago:
                        post['board_name'] = board_name
                        yield post
                    else:
                        logger.info(f"遇到其他年份 結束爬取 {board_name} 版")
                        return
                except Exception as e:
                    print(e)
                    continue

            except Exception as e:
                print(e)
                continue

        next_page = soup.select('a.btn.wide')[1]['href']
        url = f"https://www.ptt.cc{next_page}"



def run_crawler():

    ptt_boards = [ "NBA", "Lifeismoney", "home-sale", "mobilecomm","Baseball","c_chat",]
    for board in ptt_boards:
        logger.info(f"開始爬取 {board} 版的文章...")
        try:
            posts = fetch_board_posts(board)
        except Exception as e:
            logger.error(f"Error fetching posts from {board}: {str(e)}")
            continue

        for post in posts:
            db = Session()
            try:
                post['date'] = datetime.strptime(post['date'], "%Y/%m/%d %H:%M:%S")
                CreatePosts(**post)
                create_ptt_post(db, **post)

                logger.info(f"成功儲存文章: {post['title']}")

            except Exception as e:
                logger.error(f"{post['title']}: {str(e)}")
                continue

if __name__ == "__main__":
    run_crawler()