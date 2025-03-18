from starlette.status import HTTP_404_NOT_FOUND
from app.models import AuthorTable

def get_author(db, author_ptt_id:str , author_nickname:str = None, create_if_not_exists=False):
    author = db.query(AuthorTable).filter_by(author_ptt_id=author_ptt_id).first()
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
            return {'status_code':HTTP_404_NOT_FOUND,'error':'沒有這個作者'}

    return author
