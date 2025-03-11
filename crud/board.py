from app.models import *
from fastapi import HTTPException, status


def get_board_by_id(db, board_id):
    board = db.get(BoardTable,board_id)
    return board

# Todo finish get_board_by_board_name and author (finish)
def get_and_create_board(db, board_name,create_if_not_exists=False):
    board = db.query(BoardTable).filter_by(board=board_name).first()
    if not board:
        if create_if_not_exists:
            board = BoardTable(
                board=board_name,
                url=f"https://www.ptt.cc/bbs/{board_name}/index.html"
            )
            db.add(board)
            db.commit()
            db.refresh(board)

        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="沒有這個版")

    return board


def delete_board(db, board_id):
    board = get_board_by_id(db, board_id)
    db.delete(board)
    db.commit()
    return board