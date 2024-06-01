import time
from fastapi import FastAPI, Response, status, HTTPException, Depends
import psycopg2
from . import models, schemas
from .database import engine, get_db
from sqlalchemy.orm import Session
from typing import List

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


@app.get("/posts", response_model=List[schemas.Post])
async def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@app.get("/posts/{id}", response_model=schemas.Post)
async def get_post(id, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with ID {id} not found')
    return post


# using pydantic/schema model : Post in decorator to sendback custom/controlled
# response to the user
@app.post("/create_post", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # Standard approach
    # new_post = models.Post(title=post.title, content=post.content, rating=post.rating, is_active=post.is_active)
    # pydantic approach
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Post)
async def update_post(id, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with ID {id} not found so not updated')
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with ID {id} not found so not deleted')
    # Session Basic in sqlalchemy 1.4 (selecting a sync strategy)
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
