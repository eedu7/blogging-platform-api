from sqlalchemy import select
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
            "tags": get_tag_by_blog_id(db, blog.id),
            "created_at": blog.created_at,
            "updated_at": blog.updated_at,
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
        "tags": get_tag_by_blog_id(db, blog.id),
        "created_at": blog.created_at,
        "updated_at": blog.updated_at,
    }


def get_all_tags(db: Session, blog_id: int):
    return db.query(Tag).filter(Tag.blog_id == blog_id).all()


def update_or_delete_tags(db: Session, blog_id: int, tags: list):
    existings_tags = get_all_tags(db, blog_id)
    existings_tags_names = [tag.name for tag in existings_tags]

    for tag in existings_tags:
        if tag.name not in tags:
            delete_tag(db, tag.id)

    for tag in tags:
        if tag not in existings_tags_names:
            add_tag(db, tag, blog_id)


def add_tag(db: Session, tag, blog_id):
    new_tags = Tag(name=tag, blog_id=blog_id)
    db.add(new_tags)
    db.commit()
    return True


def get_tag_by_blog_id(db: Session, blog_id):
    tags = db.query(Tag).filter(Tag.blog_id == blog_id).all()
    return [tag.name for tag in tags]


def update_blog(
    db: Session,
    blog_id: int,
    title: str | None = None,
    content: str | None = None,
    category: str | None = None,
):
    try:
        blog = db.query(Blog).filter(Blog.id == blog_id).first()

        if not blog:
            return False

        if title:
            blog.title = title
        if content:
            blog.content = content

        if category:
            blog.category = category

        db.commit()
        db.refresh(blog)
        return True
    except Exception:
        return False


def delete_blog(db: Session, blog_id: int):
    try:
        blog = db.query(Blog).filter(Blog.id == blog_id).first()

        if not blog:
            return False

        db.delete(blog)
        db.commit()
        return True
    except Exception:
        return False


def delete_tag(db: Session, tag_id: int):
    try:
        tag = db.query(Tag).filter(Tag.id == tag_id).first()

        if not tag:
            return False

        db.delete(tag)
        db.commit()
        return True
    except Exception:
        return False


def delete_tags(db: Session, blog_id: int):
    try:
        tags = db.query(Tag).filter(Tag.blog_id == blog_id).all()

        if not tags:
            return False

        for tag in tags:
            db.delete(tag)

        db.commit()
        return True
    except Exception:
        return False


def search_blogs(db: Session, field: str, value):
    query = select(Blog).where(getattr(Blog, field) == value)
    blogs = db.execute(query).scalars().all()
    new_data = []
    for blog in blogs:
        data = {
            "id": blog.id,
            "title": blog.title,
            "content": blog.content,
            "category": blog.category,
            "tags": get_tag_by_blog_id(db, blog.id),
            "created_at": blog.created_at,
            "updated_at": blog.updated_at,
        }
        new_data.append(data)
    return new_data
