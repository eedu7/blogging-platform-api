from typing import List

from pydantic import BaseModel

class Base(BaseModel):
    title: str
    category: str
    content: str
    tags: List[str | None]
    
class UpdateBlog(BaseModel):
    title: str | None = None
    category: str | None = None
    content: str | None = None
    tags: List[str | None] = []

class CreateBlog(Base):
    pass

class BlogResponse(Base):
    id: int