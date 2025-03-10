from app.models import *

def get_board_by_board_name(db, board_name):
    board = db.query(BoardTable).filter_by(board=board_name).first()

    return board

def get_board_by_id(db, board_id):
    board = db.query(BoardTable).get(board_id)
    return board


def create_board(db, **ptt_post):
    board = BoardTable(
        board=ptt_post['board_name'],
        url=f"https://www.ptt.cc/bbs/{ptt_post['board_name']}/index.html"
    )
    db.add(board)
    db.commit()
    db.refresh(board)
    return board


def check_board(db, **ptt_post):
    board = get_board_by_board_name(db, ptt_post['board_name'])
    if not board:
        board = create_board(db, **ptt_post)

    return board