import time

from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2

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
async def get_all_posts():
    cur.execute("""SELECT * FROM post""")
    rows = cur.fetchall()
    column_names = [desc[0] for desc in cur.description]
    posts = [dict(zip(column_names, row)) for row in rows]
    return {"data": posts}


@app.get("/posts/{id}")
async def get_post(id, response: Response):
    cur.execute("""SELECT * FROM post WHERE id = %s """, (str(id),))
    post = cur.fetchone()
    # print(pos)
    # post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with ID {id} not found')
    return {"data": post}


@app.post("/create_post", status_code=status.HTTP_201_CREATED)
async def create_new_post(post: Post):
    post_dict = post.dict()
    post_dict['id'] = str(randrange(0, 1000000))  # Ensure id is a string
    my_posts.append(post_dict)
    return {"data": post_dict}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    cur.execute("""SELECT * FROM post WHERE id = %s""", (str(id),))
    post = cur.fetchone()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with ID {id} not found so not deleted')
    cur.execute("""DELETE FROM post WHERE id = %s""", (str(id),))
    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
async def update_post(id, post: Post):
    cur.execute("""UPDATE post SET title = %s, content = %s, is_active = %s RETURNING *""", (
        post.title, post.content, post.is_active))
    post = cur.fetchone()
    conn.commit()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with ID {id} not found so not updated')
    return {"data": post}

