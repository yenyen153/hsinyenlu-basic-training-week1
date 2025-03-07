from fastapi import FastAPI, Depends, HTTPException, Query, Request, Form, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func, and_
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
from app.databases import get_db
from app.models import PttPostsTable, BoardTable, AuthorTable
from app.schemas import *

# 初始化 FastAPI
app = FastAPI()

# 掛載靜態檔案
app.mount("/static", StaticFiles(directory="static"), name="static")

# 設定模板目錄
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/posts",response_model=list[PostResponse])
async def get_posts(
        request: Request,
        db: Session = Depends(get_db),
        limit: int = Query(50, ge=1, le=100, description="每次查詢的最多文章數"),
        offset: int = Query(0, ge=0, description="要跳過的文章數"),
        board_name: str = Query(None, description="版面"),
        author_ptt_id: str = Query(None, description="作者 PTT ID"),
        post_date: datetime = Query(None, description="發文日期 (YYYY-MM-DD 格式)"),
):
    query = db.query(PttPostsTable)

    if board_name:
        board = db.query(BoardTable).filter(BoardTable.board == board_name).first()
        if not board:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="沒有這個版面")
        query = query.filter(PttPostsTable.board_id == board.id)

    if author_ptt_id:
        author = db.query(AuthorTable).filter(AuthorTable.author_ptt_id == author_ptt_id).first()
        if not author:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="沒有這個作者")
        query = query.filter(PttPostsTable.author_id == author.id)

    if post_date:
        try:
            start_date = post_date.strftime("%Y/%m/%d 00:00:00")  #先換成字串
            end_date = (post_date + timedelta(days=1)).strftime("%Y/%m/%d 00:00:00")
            query = query.filter(PttPostsTable.date >= start_date, PttPostsTable.date < end_date)

        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="錯誤的日期格式，請使用 YYYY-MM-DD")

    query = query.order_by(PttPostsTable.date.desc())
    posts = query.offset(offset).limit(limit).all()

    for post in posts:
        post.date = datetime.strptime(post.date, "%Y/%m/%d %H:%M:%S")  #

    return posts

@app.get("/posts/{post_id}", response_model=PostResponse)
async def get_post(post_id: int, request: Request, db: Session = Depends(get_db)):
    post = db.get(PttPostsTable, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="找不到這篇文章")
    post.date = datetime.strptime(post.date, "%Y/%m/%d %H:%M:%S")
    return post


@app.get("/statistics")
async def get_statistics(
        request: Request,
        post_date: datetime = Query(None, description="發文日期 (YYYY-MM-DD)"),
        board_name: str = Query(None, description="版面名稱"),
        author_ptt_id: str = Query(None, description="作者 PTT ID"),
        db: Session = Depends(get_db)
):
    query = db.query(func.count(PttPostsTable.id))
    filters = []

    if board_name:
        board = db.query(BoardTable).filter(BoardTable.board == board_name).first()
        if board:
            filters.append(PttPostsTable.board_id == board.id)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="沒有這個版面")

    if author_ptt_id:
        author = db.query(AuthorTable).filter(AuthorTable.author_ptt_id == author_ptt_id).first()
        if author:
            filters.append(PttPostsTable.author_id == author.id)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="沒有這個作者")

    if post_date:
        try:
            post_date_str = post_date.strftime("%Y/%m/%d")
            filters.append(PttPostsTable.date.like(f"{post_date_str}%"))
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="錯誤的日期格式 請用 YYYY-MM-DD")


    if filters:
        query = query.filter(and_(*filters))

    total_posts = query.scalar()

    return {"文章總篇數": total_posts}

@app.post("/api/posts", response_model=PostResponse)
async def create_post(post: CreatePosts, db: Session = Depends(get_db)):
    board = db.query(BoardTable).filter(BoardTable.board == post.board_name).first()
    if not board:
        board = BoardTable(
            board=post.board_name,
            url=f"https://www.ptt.cc/bbs/{post.board_name}/index.html"
        )
        db.add(board)
        db.commit()
        db.refresh(board)

    author = db.query(AuthorTable).filter(AuthorTable.author_ptt_id == post.author_ptt_id).first()
    if not author:
        author = AuthorTable(
            author_nickname=post.author_nickname,
            author_ptt_id=post.author_ptt_id
        )
        db.add(author)
        db.commit()
        db.refresh(author)


    existing_post = db.query(PttPostsTable).filter(PttPostsTable.link == post.link).first()
    if existing_post:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="貼文已經存在")

    db_post = PttPostsTable(
        title=post.title,
        link=str(post.link),
        date=post.date.strftime("%Y/%m/%d %H:%M:%S"),
        content=post.content,
        board_id=board.id,
        author_id=author.id
    )  # todo: 這便直接用crud的工具 不要有ｄｂ操作

    db.add(db_post)
    try:
        db.commit()
        db.refresh(db_post)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="貼文已經存在")
    db_post.date = datetime.strptime(db_post.date, "%Y/%m/%d %H:%M:%S")

    return db_post

@app.put("/api/posts/{post_id}", response_model=PostResponse)
async def update_post(post_id: int, post_update: CreatePosts, db: Session = Depends(get_db)):

    db_post = db.get(PttPostsTable,post_id)
    if db_post is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="沒有這篇貼文")

    board = db.query(BoardTable).filter(BoardTable.board == post_update.board_name).first()
    if not board:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="沒有這個版")

    author = db.query(AuthorTable).filter(AuthorTable.author_ptt_id == post_update.author_ptt_id).first()
    if not author:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="沒有這個作者")

    db_post.title = post_update.title
    db_post.link = post_update.link
    db_post.date = post_update.date.strftime("%Y/%m/%d %H:%M:%S")
    db_post.content = post_update.content
    db_post.board_id = board.id
    db_post.author_id = author.id

    try:
        db.commit()
        db.refresh(db_post)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="這篇文章已經存在了")

    db_post.date = datetime.strptime(db_post.date, "%Y/%m/%d %H:%M:%S")

    return db_post

@app.delete("/delete/{post_id}")
async def delete_post(post_id: int, request: Request, db: Session = Depends(get_db)):
    post = db.get(PttPostsTable, post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="找不到這篇文章")

    db.delete(post)
    db.commit()

    return {"message": "文章刪除成功"}