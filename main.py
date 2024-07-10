from fastapi import FastAPI, HTTPException, Query
import uvicorn
from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID, uuid4
from datetime import datetime

app = FastAPI()

# Pydantic Model
class Blog(BaseModel):
    id: Optional[UUID] = None
    title: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    datetime: Optional[str] = None
    
# In-Memory database
blogs = []

@app.get("/")
def getTest():
    return {"test":"success"}

# create a blog
@app.post("/create-blog", response_model=Blog)
def create_blog(blog: Blog):
    blog.id = uuid4()
    blog.datetime = str(datetime.now())
    
    blogs.append(blog)
    
    return blog

# get all blogs
@app.get("/get-blogs", response_model=List[Blog])
def get_blogs():
    return blogs

# get blog by id
@app.get("/get-blog/{blog_id}", response_model=Blog)
def get_blog(blog_id: UUID):
    for blog in blogs:
        if blog_id == blog.id:
            return blog
    raise HTTPException(status_code=404, detail="blog not found")

# get blogs by category
@app.get("/get-blogs-by-category", response_model=List[Blog])
def get_blogs_by_category(category: str = Query(...)):
    filtered_blogs = list(filter(lambda blog: blog.category == category, blogs))
    
    if len(filtered_blogs) != 0 :
        return filtered_blogs
    
    raise HTTPException(status_code=404, detail="category not found")

# update blog by id
@app.put("/update-blog/{blog_id}", response_model=Blog)
def update_blog(blog_id: UUID, updated_blog: Blog):
    for index, blog in enumerate(blogs):
        if blog.id == blog_id:
            updated_blog = blog.copy(update=updated_blog.dict(exclude_unset=True))
            blogs[index] = updated_blog
        
            return blogs[index]
        
    raise HTTPException(status_code=404, detail="blog not found")
    
# delete blog by id
@app.delete("/delete-blog/{blog_id}", response_model=Blog)
def delete_blog(blog_id: UUID):
    for index, blog in enumerate(blogs):
        if blog.id == blog_id:
            return blogs.pop(index)
    
    raise HTTPException(status_code=404, detail="blog not found")

    
if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=3000)
