from app.models import *

def open_ptt_post_by_link(db, link):
    return db.query(PttPostsTable).filter_by(link=link).first()

def open_ptt_post_by_id(db,post_id):
    post = db.get(PttPostsTable,post_id)

    return post

