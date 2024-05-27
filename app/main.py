from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional
from random import randrange

# title str, content str
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None



my_posts = [
    {"id": "1", "title": "post title", "content": "post content"},
    {"id": "2", "title": "post title 2", "content": "post content 2"}
    ]

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
    return {"data": my_posts}

@app.get("/posts/{id}")
async def get_post(id, response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'post with ID {id} not found')
    return {"data": post}
    

@app.post("/create_post", status_code=status.HTTP_201_CREATED)
async def create_new_post(post: Post):
    post_dict = post.dict()
    post_dict['id'] = str(randrange(0, 1000000))  # Ensure id is a string
    my_posts.append(post_dict)
    return {"data": post_dict}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id):
    # deleting the post
    # find the index in the array that has required ID
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'post with ID {id} not found so not deleted')
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
async def update_post(id, post: Post):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'post with ID {id} not found so not updated')
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {"data": post_dict}


