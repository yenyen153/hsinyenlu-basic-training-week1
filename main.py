from fastapi import FastAPI, Depends, Query, Request
from sqlalchemy.orm import Session
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
from app.databases import get_db
from crud.post import *

app = FastAPI()



static_dir = Path(__file__).resolve().parent / "static"
app.mount("/static", StaticFiles(directory=static_dir), name="static")

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})



@app.get("/posts/{post_id}", response_model=PostResponse)
async def get_post(post_id: int, db: Session = Depends(get_db)):
    try:
        post = get_post_by_id(db, post_id)
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="找不到這則文章！")
    return post



@app.delete("/delete/{post_id}")
async def delete_post(post_id: int, db: Session = Depends(get_db)):
    try:
        delete_post_by_id(db, post_id)
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="找不到這篇文章")

    return "文章刪除成功"


@app.get("/posts", response_model=list[PostResponse])
async def get_posts(
        db: Session = Depends(get_db),
        limit: int = Query(50, ge=1, le=100, description="每次查詢的最多文章數"),
        offset: int = Query(0, ge=0, description="要跳過的文章數"),
        board_name: str = Query(None, description="版面"),
        author_ptt_id: str = Query(None, description="作者 PTT ID"),
        post_date: datetime = Query(None, description="發文日期 (YYYY-MM-DD 格式)"),
):
    posts = get_filtered_posts(db, limit, offset, post_date, board_name, author_ptt_id)

    return posts


@app.get("/statistics")
async def get_statistics(
        post_date: datetime = Query(None, description="發文日期 (YYYY-MM-DD)"),
        board_name: str = Query(None, description="版面名稱"),
        author_ptt_id: str = Query(None, description="作者 PTT ID"),
        db: Session = Depends(get_db)
):
    posts_total = get_statistics_data(db, post_date, board_name, author_ptt_id)

    return {"文章總篇數": posts_total}


@app.post("/api/posts", response_model=PostResponse)
async def create_post(post: CreatePosts, db: Session = Depends(get_db)):
    new_post = input_post(db,**dict(post))

    return new_post

@app.put("/api/posts/{post_id}", response_model=PostResponse)
async def update_post(post_id: int, post_update: CreatePosts, db: Session = Depends(get_db)):
    updated_post = update_post_data(db, post_id, **dict(post_update))

    return updated_post

@app.delete("/delete_board/{board_id}")
async def delete_board(board_id: int, db: Session = Depends(get_db)):
    try:
        board_crud.delete_board(db, board_id)
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="wrong 請檢查是否有文章或該版面存在")

    return  "版面刪除成功"


@app.get("/api/board/{board_id}")
async def get_board(board_id: int, db: Session = Depends(get_db)):
    try:
        board = board_crud.get_board_by_id(db,board_id)
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="找不到這個版面")
    return board
