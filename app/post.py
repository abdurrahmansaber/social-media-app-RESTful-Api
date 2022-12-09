from pydantic import BaseModel
from typing import Optional

class Post(BaseModel):
    title: str
    content: str
    is_published: bool = True
    rating: Optional[int] = None