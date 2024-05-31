import time
from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

while True:
    try:
        conn = psycopg2.connect(host="localhost", database="fastAPI_blog", user="postgres", password="admin1122")
        cur = conn.cursor()
        cur.execute("SELECT version();")
        record = cur.fetchone()
        print("You are connected to: ", record, "\n")
        break
    except Exception as error:
        print("Unable to establish database connection.")
        print(f"Error Detail: {error}")
        time.sleep(5)


# title str, content str
class Post(BaseModel):
    title: str
    content: str
    is_active: bool = True
    rating: Optional[int] = None


my_posts = [{"id": "1", "title": "post title", "content": "post content"},
            {"id": "2", "title": "post title 2", "content": "post content 2"}]


def find_post(id: int):
    for p in my_posts:
        if p["id"] == id:
            return p


def find_index_post(id: int):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i


app = FastAPI()


@app.get("/")
async def root():
    return {"data": "Main Page"}


@app.get("/posts")
async def get_all_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}


@app.get("/posts/{id}")
async def get_post(id, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with ID {id} not found')
    return {"data": post}


@app.post("/create_post", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post, db: Session = Depends(get_db)):
    # Standard approach
    # new_post = models.Post(title=post.title, content=post.content, rating=post.rating, is_active=post.is_active)
    # pydantic approach
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    cur.execute("""SELECT * FROM post WHERE id = %s""", (str(id),))
    post = cur.fetchone()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with ID {id} not found so not deleted')
    cur.execute("""DELETE FROM post WHERE id = %s""", (str(id),))
    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
async def update_post(id, post: Post, db: Session = Depends(get_db)):
    # update_post = models.Post(**post.dict())
    post_update = db.query(models.Post).filter(models.Post.id == id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with ID {id} not found so not updated')
    post_update.title = post.title
    post_update.content = post.content
    post_update.rating = post.rating
    post_update.is_active = post.is_active
    db.commit()
    db.refresh(update_post)
    return {"data": update_post}
