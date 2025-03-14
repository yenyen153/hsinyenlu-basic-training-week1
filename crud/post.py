from fastapi import HTTPException, status
from sqlalchemy import func, and_
from sqlalchemy.exc import IntegrityError
import crud.author as author_crud
import crud.board as board_crud
from app.schemas import *
from app.models import *
from datetime import timedelta



def get_post_by_link(db, link):
    post = db.get(PttPostsTable,link)

    return post


def get_post_by_id(db, post_id:int, delete_or_not=False):
    post = db.get(PttPostsTable, post_id)
    if post:
        if delete_or_not:
            db.delete(post)
            db.commit()

        else:
            try:
                post.date = datetime.strptime(post.date, "%Y/%m/%d %H:%M:%S")
            except:
                post.date = post.date
            return post
    else:
        return {'error':"沒有這篇貼文"}


def common_filters(db, query, start_date: datetime = None, end_date: datetime = None, board_name: str = None, author_ptt_id: str = None):
    filters = []

    if board_name:
        board = board_crud.get_and_create_board(db, board_name)
        try:
            filters.append(PttPostsTable.board_id == board.id)
        except:
            return {'error': '沒有這版面'}

    if author_ptt_id:
        author = author_crud.get_author(db, author_ptt_id) # todo
        if isinstance(author,dict) and "error" in author:
            return author
        else:
            filters.append(PttPostsTable.author_id == author.id)

    if start_date and end_date:
        try:
            start_date_str = start_date.strftime("%Y/%m/%d")
            end_date_str = (end_date + timedelta(days=1)).strftime("%Y/%m/%d")
            filters.append(PttPostsTable.date.between(start_date_str, end_date_str))
        except ValueError:
            return {'error': "錯誤的日期格式!!!請使用YYYY-MM-DD"}

    if filters:
        query = query.filter(and_(*filters))

    return query


def get_statistics_data(db, start_date: datetime = None, end_date: datetime = None, board_name: str = None,
                        author_ptt_id: str = None):
    query = db.query(func.count(PttPostsTable.id))
    query = common_filters(db, query, start_date, end_date, board_name, author_ptt_id)

    try:
        posts_total = query.scalar()
    except:
        return query

    return posts_total


def get_filtered_posts(db, limit: int, offset: int, start_date: datetime = None, end_date: datetime = None, board_name: str = None, author_ptt_id: str = None):
    query = db.query(PttPostsTable)
    query = common_filters(db, query, start_date, end_date, board_name, author_ptt_id)
    try:
        query = query.order_by(PttPostsTable.date.desc())
        posts = query.offset(offset).limit(limit).all()
    except: # todo
        return query

    for post in posts:
        try:
            post.date = datetime.strptime(post.date, "%Y/%m/%d %H:%M:%S")
        except:
            post.date = post.date


    return posts


def refresh_db(db, post):
    try:
        db.commit()
        db.refresh(post)
    except IntegrityError:
        db.rollback()
        return {'error':'貼文已存在'}

    post.date = datetime.strptime(post.date, "%Y/%m/%d %H:%M:%S")

    return post


def update_post_data(db, post_id: int, **post_update):
    post = db.get(PttPostsTable, post_id)
    if post is None:

        return {'status_code':status.HTTP_404_NOT_FOUND,'error':'貼文不存在'}

    board = board_crud.get_and_create_board(db,post_update['board_name'])
    author = author_crud.get_author(db, post_update['author_ptt_id'], post_update['author_nickname'])

    if isinstance(post_update["date"], str):
        try:
            post_update["date"] = datetime.strptime(post_update["date"], "%Y-%m-%dT%H:%M:%S")
        except ValueError:
            return {'status_code':status.HTTP_400_BAD_REQUEST,"error":"日期格式錯誤"}

    if isinstance(board, dict) and "error" in board:
        return board
    if isinstance(author, dict) and "error" in author:
        return author

    post.title = post_update["title"]
    post.link = str(post_update["link"])
    post.date = post_update["date"].strftime("%Y/%m/%d %H:%M:%S")
    post.content = post_update["content"]
    post.board_id = board.id
    post.author_id = author.id

    post = refresh_db(db, post)

    return post

def create_ptt_post(db, **ptt_post):
    post = db.get(PttPostsTable, ptt_post['link'])
    board = board_crud.get_and_create_board(db,ptt_post['board_name'], create_if_not_exists=True)
    author = author_crud.get_author(db, ptt_post['author_ptt_id'], ptt_post['author_nickname'], create_if_not_exists=True)

    if post:
        return {'error':'貼文已存在'}

    new_ptt_post = PttPostsTable(
        board_id=board.id,
        title=ptt_post['title'],
        link=str(ptt_post['link']),
        author_id=author.id,
        date=ptt_post['date'].strftime("%Y/%m/%d %H:%M:%S"),
        content=ptt_post['content']
    )

    db.add(new_ptt_post)
    new_ptt_post = refresh_db(db, new_ptt_post)

    return new_ptt_post
