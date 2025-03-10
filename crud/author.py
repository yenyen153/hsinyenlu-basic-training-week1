from app.models import *


def get_author_by_ptt_id(db, author_ptt_id):
    author = db.query(AuthorTable).filter_by(author_ptt_id=author_ptt_id).first()

    return author


def get_author_by_id(db, author_id):
    author = db.query(AuthorTable).get(author_id)
    return author

def create_author(db, **ptt_post):
    author = AuthorTable(
        author_nickname=ptt_post['author_nickname'],
        author_ptt_id=ptt_post['author_ptt_id'],
    )
    db.add(author)
    db.commit()
    db.refresh(author)
    return author


def check_author(db, **ptt_post):
    author = get_author_by_ptt_id(db, ptt_post['author_ptt_id'])
    if not author:
        author = create_author(db, **ptt_post)

    return author