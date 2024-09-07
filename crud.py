from sqlalchemy.orm import Session
from model import Blog, Tag

def add_blog(db: Session, title: str, content: str, category: str):
    new_blog = Blog(title=title, content=content, category=category)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

def get_all_blogs(db: Session):
    blogs = db.query(Blog).all()
    new_data = []
    for blog in blogs:
        data = {
            "id": blog.id,
            "title": blog.title,
            "content": blog.content,
            "category": blog.category,
            "tags": get_tag_by_blog_id(db, blog.id)
        }
        new_data.append(data)
    return new_data

def get_by_id(db: Session, blog_id: int):
    blog = db.query(Blog).filter(Blog.id == blog_id).first()
    return {
        "id": blog.id,
        "title": blog.title,
        "content": blog.content,
        "category": blog.category,
        "tags": get_tag_by_blog_id(db, blog.id)
    }

def add_tag(db: Session, tag, blog_id):
    new_tags = Tag(name=tag, blog_id=blog_id)
    db.add(new_tags)
    db.commit()
    return True

def get_tag_by_blog_id(db: Session, blog_id):
    tags = db.query(Tag).filter(Tag.blog_id == blog_id).all()
    return [tag.name for tag in tags]