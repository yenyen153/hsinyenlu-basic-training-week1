from app.models import *
from fastapi import HTTPException, status

def get_author_by_ptt_id(db, author_ptt_id):
    author = db.query(AuthorTable).filter_by(author_ptt_id=author_ptt_id).first()
    return author


def get_and_create_author(db, author_ptt_id, author_nickname,create_if_not_exists=False):
    author = get_author_by_ptt_id(db, author_ptt_id)
    if not author:
        if create_if_not_exists:
            author = AuthorTable(
                author_ptt_id=author_ptt_id,
                author_nickname=author_nickname
            )
            db.add(author)
            db.commit()
            db.refresh(author)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="沒有作者")

    return author
