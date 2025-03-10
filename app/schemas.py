from pydantic import BaseModel, HttpUrl, field_validator, Field
import re
from datetime import datetime

# class PttPostModel(BaseModel):
#     board_name: str
#     title: str
#     link: HttpUrl
#     author_ptt_id: str
#     date: str
#     author_nickname: str
#     content: str
#
#     @field_validator('date')
#     @classmethod
#     def validate_date(cls, value:str) -> str:
#         if not re.search(r"\d{4}[/]\d{2}[/]\d{2}\s\d{2}[:]\d{2}[:]\d{2}", value):
#             raise ValueError('wrong date format')
#         return value
# 這邊 直接使用createPosts來創建

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
