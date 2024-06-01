from pydantic import BaseModel, EmailStr
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


class UserCreate(BaseModel):
    full_name: str
    username: str
    # pydantic Types EmailStr doc
    email: EmailStr
    password: str


class User(BaseModel):
    id: int
    full_name: str
    username: str
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    tokey_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
