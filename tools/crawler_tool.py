import requests
from bs4 import BeautifulSoup
from datetime import datetime


PTT_URL = "https://www.ptt.cc/bbs/{}/index.html"

session = requests.Session()
session.cookies.set("over18", "1")


#爬取link
def fetch_link(board):
    res = session.get(PTT_URL.format(board))
    soup = BeautifulSoup(res.text, "html.parser")
    articles = soup.select(".r-ent")

    links = []
    for article in articles:
        title_elem = article.select_one(".title a")
        if not title_elem:
            continue


        post_link = f"https://www.ptt.cc{title_elem['href']}"

        links.append(post_link)

    return links

## 爬取內文
def fetch_content(link):
    res = requests.get(link)
    soup = BeautifulSoup(res.text, "html.parser")
    content = soup.find(id="main-content").text
    end_point = u'※ 發信站: 批踢踢實業坊(ptt.cc),'
    content = content.split(end_point)
    return content[0]

def fetch_post_detail(link):
    res = requests.get(link)
    soup = BeautifulSoup(res.text, "html.parser")
    if soup.select(".article-meta-value"):
        post_details = soup.select(".article-meta-value")
        details_list = []

        for author in post_details:
            details_list.append(author.text)

        posts_detail = {
            'title':details_list[2],
            'author_ptt_id':((details_list[0].split('('))[0]).rstrip(),
            'author_nickname':((details_list[0].split('('))[1]).rstrip(')') if (details_list[0].split('('))[1] else "no nickname"
        }

        time_str = details_list[-1]
        dt = datetime.strptime(time_str, "%a %b %d %H:%M:%S %Y")
        formatted_time = dt.strftime("%Y/%m/%d %H:%M:%S")
        posts_detail['date'] = formatted_time
        posts_detail['content'] = fetch_content(link)
        posts_detail['link'] = link
    else:
        posts_detail = "No detail"

    return posts_detail