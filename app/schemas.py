from pydantic import BaseModel, HttpUrl
from datetime import datetime

class CreatePosts(BaseModel):
    board_name: str
    title: str
    link: HttpUrl
    author_ptt_id: str
    date: datetime
    author_nickname: str
    content: str

    class Config:
        from_attributes = True


class PostResponse(BaseModel):
    id: int
    title: str
    link: HttpUrl
    date: datetime
    board_id: int
    author_id: int
    content: str

    class Config:
        from_attributes = True
