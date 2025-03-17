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

    result = get_post_by_id(db, post_id)

    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=result['status_code'], detail=result['error'])

    return result



@app.delete("/delete/{post_id}")
async def delete_post(post_id: int, db: Session = Depends(get_db)):
    result = get_post_by_id(db, post_id,delete_or_not=True)
    if isinstance(result,dict) and "error" in result:
        raise HTTPException(status_code=result['status_code'], detail=result['error'])

    return "文章刪除成功"


@app.get("/posts", response_model=list[PostResponse])
async def get_posts(
        db: Session = Depends(get_db),
        limit: int = Query(50, ge=1, le=100, description="每次查詢的最多文章數"),
        offset: int = Query(0, ge=0, description="要跳過的文章數"),
        board_name: str = Query(None, description="版面"),
        author_ptt_id: str = Query(None, description="作者PTT ID"),
        start_date: datetime = Query(None, description="開始日期 (YYYY-MM-DD)"),
        end_date: datetime = Query(None, description="結束日期 (YYYY-MM-DD)"),
):
    result = get_filtered_posts(db, limit, offset, start_date, end_date, board_name, author_ptt_id)

    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=result['status_code'], detail=result['error'])

    return result


@app.get("/statistics")
async def get_statistics(
        start_date: datetime = Query(None, description="開始日期 (YYYY-MM-DD)"),
        end_date: datetime = Query(None, description="結束日期 (YYYY-MM-DD)"),
        board_name: str = Query(None, description="版面"),
        author_ptt_id: str = Query(None, description="作者PTT ID"),
        db: Session = Depends(get_db)
):
    result = get_statistics_data(db, start_date, end_date, board_name, author_ptt_id)
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=result['status_code'], detail=result['error'])

    return {"post_total": result}


@app.post("/api/posts", response_model=PostResponse)
async def create_post(post: CreatePosts, db: Session = Depends(get_db)):

    result = create_ptt_post(db, **dict(post))
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=result['status_code'], detail=result['error'])

    return result


@app.put("/api/posts/{post_id}", response_model=PostResponse)
async def update_post(post_id: int, post_update: CreatePosts, db: Session = Depends(get_db)):
    result = update_post_data(db, post_id, **dict(post_update))

    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=result['status_code'], detail=result["error"])

    return result
