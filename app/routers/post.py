from typing import List
from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from fastapi import Response, status, HTTPException, Depends, APIRouter

router = APIRouter(prefix="/posts", tags=['Posts'])


@router.get("/", response_model=List[schemas.Post])
async def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@router.get("/my_posts", response_model=List[schemas.Post])
async def get_my_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    return posts


@router.get("/{id}", response_model=schemas.Post)
async def get_post(id, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with ID {id} not found')
    return post


# using pydantic/schema model : Post in decorator to sendback custom/controlled
# response to the user
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_post(post: schemas.PostCreate, db: Session = Depends(get_db),
                      current_user: int = Depends(oauth2.get_current_user)):
    # Standard approach
    # new_post = models.Post(title=post.title, content=post.content, rating=post.rating, is_active=post.is_active)
    # pydantic approach
    # print(current_user.email)
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Post)
async def update_post(id, updated_post: schemas.PostCreate, db: Session = Depends(get_db),
                      current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with ID {id} not found so not updated')
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested actions.")
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with ID {id} not found so not deleted')
    # Session Basic in sqlalchemy 1.4 (selecting a sync strategy)
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested actions.")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
