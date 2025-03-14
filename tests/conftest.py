import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from main import app
from app.databases import Base, get_db
from app.models import PttPostsTable, BoardTable, AuthorTable


@pytest.fixture(scope="function")
def db_session():
    SQLITE_DATABASE_URL = "sqlite:///:memory:"

    engine = create_engine(
        SQLITE_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )

    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    session = Session()
    yield session
    session.close()


@pytest.fixture(scope="function")
def setup_test_data(db_session):

    board = BoardTable(board="board_name for testing", url="https://www.ptt.cc/bbs/test/index.html")
    db_session.add(board)
    db_session.commit()


    author = AuthorTable(author_ptt_id="author_ptt_id for testing", author_nickname="author_nickname for testing")
    db_session.add(author)
    db_session.commit()

    post = PttPostsTable(
        title="title for testing",
        link="https://linkfortesting.com/",
        date="2024/10/08 12:34:10",
        content="content for testing",
        board_id=board.id,
        author_id=author.id
    )
    db_session.add(post)
    db_session.commit()
    db_session.refresh(post)

    yield post

    db_session.delete(post)
    db_session.delete(author)
    db_session.delete(board)
    db_session.commit()



@pytest.fixture(scope="function")
def test_client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client