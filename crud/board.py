from app.models import *

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
            return {'error': "沒有這個版面"}

    return board

