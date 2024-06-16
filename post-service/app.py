from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
import time
import sqlalchemy.exc

app = FastAPI()

DATABASE_URL = "postgresql://user:password@db:5432/user_db"

# ベースモデルを一度だけインスタンス化
Base = declarative_base()


# リトライロジックを追加してデータベース接続を確立
def connect_to_database():
    retries = 5
    delay = 1
    while retries > 0:
        try:
            engine = create_engine(DATABASE_URL)
            SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
            return engine, SessionLocal
        except sqlalchemy.exc.OperationalError:
            print(
                f"Failed to connect to database. Retrying in {delay} seconds... ({retries} retries left)"
            )
            time.sleep(delay)
            delay *= 2
            retries -= 1
    raise Exception("Failed to connect to the database after multiple attempts")


engine, SessionLocal = connect_to_database()


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)
    author_id = Column(Integer)


# Pydanticモデルの定義
class PostCreate(BaseModel):
    title: str
    content: str
    author_id: int


# データベースセッションの依存関係
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/posts/", response_model=PostCreate)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    db_post = Post(title=post.title, content=post.content, author_id=post.author_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post
