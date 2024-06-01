from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# Schema Models
# Schema/Pydantic Models define the structure of a Request & Response
# Way to handle validations in a more flexible way
class PostBase(BaseModel):
    title: str
    content: str
    is_active: bool = True
    rating: Optional[int] = None


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
