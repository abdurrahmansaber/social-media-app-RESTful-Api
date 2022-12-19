from datetime import datetime

from pydantic import BaseModel, EmailStr
from typing import Optional



class Post(BaseModel):
    title: str
    content: str
    is_published: bool = True
    rating: Optional[int] = None

    class Config:
        orm_mode = True

class CreatePost(Post):
    pass


class ResponsePost(Post):
    id: int
    create_date: datetime
    rating: int
    owner_id : int


class BaseUser(BaseModel):
    email: EmailStr

    class Config:
        orm_mode = True


class UserCreate(BaseUser):
    password: str


class UserResponse(BaseUser):
    id: int
    create_date: datetime
    pass


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id :Optional[str] = None
