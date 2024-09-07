from typing import List

from pydantic import BaseModel

class Base(BaseModel):
    title: str
    category: str
    content: str
    tags: List[str]

class CreateBlog(Base):
    pass

class BlogResponse(Base):
    id: int