from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi.responses import  JSONResponse
from db import get_db, Base, engine
import schema
import crud
app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/", status_code=200)
def get_all_blogs(db: Session = Depends(get_db)):
    return crud.get_all_blogs(db)

@app.get("/{blog_id}", status_code=200)
def get_blog(blog_id: int, db: Session = Depends(get_db)):
    return crud.get_by_id(db, blog_id)


@app.post("/", response_model=schema.BlogResponse, status_code=200)
def create_a_blog(blog: schema.CreateBlog, db:Session = Depends(get_db)):
    new_blog = crud.add_blog(db, blog.title, blog.content, blog.category)
    if blog.tags:
        for tag in blog.tags:
            crud.add_tag(db, blog_id=new_blog.id, tag=tag)

    return JSONResponse(status_code=201, content={"message": "Blog created successfully"})

@app.put("/{blog_id}")
def update_a_blog(blog_id: int, blog: schema.UpdateBlog, db:Session = Depends(get_db)):
    updated_blog = crud.update_blog(db, blog_id, blog.title, blog.content, blog.category)
    return updated_blog