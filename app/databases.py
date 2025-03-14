from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


engine = create_engine(
    "mysql+pymysql://user:password@localhost/ptt_db?charset=utf8mb4",
    connect_args={"charset": "utf8mb4"}

)

Session = sessionmaker(bind=engine)
Base = declarative_base()


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()