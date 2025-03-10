from fastapi import HTTPException, status
from sqlalchemy import func, and_
from sqlalchemy.exc import IntegrityError
import crud.ptt_posts as post_crud
import crud.author as author_crud
import crud.board as board_crud
from app.schemas import *
from app.models import *


def get_post_by_id(db, post_id):
    post = post_crud.open_ptt_post_by_id(db, post_id)
    try:
        post.date = datetime.strptime(post.date, "%Y/%m/%d %H:%M:%S")
    except:
        post.date = post.date
    return post


def delete_post_by_id(db, post_id):
    post = post_crud.open_ptt_post_by_id(db, post_id)
    db.delete(post)
    db.commit()


def common_filters(db, query, post_date: datetime = None, board_name: str = None, author_ptt_id: str = None):
    filters = []

    if board_name:
        board = board_crud.get_board_by_board_name(db, board_name)
        if board:
            filters.append(PttPostsTable.board_id == board.id)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="沒有這個版面")

    if author_ptt_id:
        author = author_crud.get_author_by_ptt_id(db, author_ptt_id)
        if author:
            filters.append(PttPostsTable.author_id == author.id)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="沒有這個作者")

    if post_date:
        try:
            post_date_str = post_date.strftime("%Y/%m/%d")
            filters.append(PttPostsTable.date.like(f"{post_date_str}%"))
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="錯誤的日期格式，請使用 YYYY-MM-DD")

    if filters:
        query = query.filter(and_(*filters))

    return query


def get_statistics_data(db, post_date: datetime = None, board_name: str = None, author_ptt_id: str = None):
    query = db.query(func.count(PttPostsTable.id))
    query = common_filters(db, query, post_date, board_name, author_ptt_id)
    posts_total = query.scalar()

    return posts_total


def get_filtered_posts(db, limit: int, offset: int, post_date: datetime = None, board_name: str = None,
                       author_ptt_id: str = None):
    query = db.query(PttPostsTable)
    query = common_filters(db, query, post_date, board_name, author_ptt_id)

    query = query.order_by(PttPostsTable.date.desc())
    posts = query.offset(offset).limit(limit).all()

    for post in posts:
        try:
            post.date = datetime.strptime(post.date, "%Y/%m/%d %H:%M:%S")
        except:
            post.date = post.date

    return posts


def update_post_data(db, post_id, **post_update):
    post = post_crud.open_ptt_post_by_id(db, post_id)
    if post is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="沒有這篇貼文")

    board = board_crud.get_board_by_board_name(db, post_update['board_name'])
    if not board:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="沒有這個版")

    author = author_crud.get_author_by_ptt_id(db, post_update['author_ptt_id'])
    if not author:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="沒有這個作者")


    if isinstance(post_update["date"], str):
        try:
            post_update["date"] = datetime.strptime(post_update["date"], "%Y-%m-%dT%H:%M:%S")
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="日期格式錯誤")

    post.title = post_update["title"]
    post.link = str(post_update["link"])
    post.date = post_update["date"].strftime("%Y/%m/%d %H:%M:%S")
    post.content = post_update["content"]
    post.board_id = board.id
    post.author_id = author.id

    try:
        db.commit()
        db.refresh(post)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="這篇文章已經存在了")

    post.date = datetime.strptime(post.date, "%Y/%m/%d %H:%M:%S")

    return post


def data_check(db, **ptt_post):
    author = author_crud.get_author_by_ptt_id(db, ptt_post['author_ptt_id'])
    board = board_crud.get_board_by_board_name(db, ptt_post['board_name'])

    if not author:
        author = board_crud.create_board(db,**ptt_post)

    if not board:
        board = board_crud.create_board(db,**ptt_post)

    return board, author


def data_in(db, **ptt_post):
    post = post_crud.open_ptt_post_by_link(db, ptt_post['link'])
    if post:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='貼文已經存在')

    board, author = data_check(db, **ptt_post)

    new_ptt_post = PttPostsTable(
        board_id=board.id,
        title=ptt_post['title'],
        link=str(ptt_post['link']),
        author_id=author.id,
        date=ptt_post['date'].strftime("%Y/%m/%d %H:%M:%S"),
        content=ptt_post['content']
    )

    db.add(new_ptt_post)

    try:
        db.commit()
        db.refresh(new_ptt_post)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="貼文已經存在")

    new_ptt_post.date = datetime.strptime(new_ptt_post.date, "%Y/%m/%d %H:%M:%S")

    return new_ptt_post
