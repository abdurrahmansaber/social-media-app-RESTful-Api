from datetime import datetime

from pydantic import BaseModel, EmailStr
from typing import Optional


class BasePost(BaseModel):
    title: str
    content: str
    is_published: bool = True
    rating: Optional[int] = None

    class Config:
        orm_mode = True


class Post(BasePost):
    pass


class ResponsePost(BasePost):
    id: int
    create_date: datetime
    rating: int


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
