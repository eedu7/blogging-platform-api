from sqlalchemy import String, Text, Integer, Column, ForeignKey
from sqlalchemy.orm import relationship
from db import Base

class Blog(Base):
    __tablename__ = 'blog'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    category = Column(String)
    content = Column(Text)


class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    blog_id = Column(Integer, ForeignKey('blog.id'))
