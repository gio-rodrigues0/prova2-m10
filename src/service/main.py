from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from logging_config import LoggerSetup
import logging

# Cria um logger raiz
logger_setup = LoggerSetup()

# Adiciona o logger para o módulo
LOGGER = logging.getLogger(__name__)

app = FastAPI()

class BlogPost(BaseModel):
    id: int
    title: str
    content: str

blog_posts = []

@app.post("/service/blog")
async def create_blog_post(blog_post: BlogPost):
    blog_posts.append(blog_post)
    return {"status": "sucesso"}, 201

@app.get("/service/blog")
async def get_blog_posts():
    return {"posts": [blog_post.dict() for blog_post in blog_posts]}

@app.get("/service/blog/{id}")
async def get_blog_post(id: int):
    for blog_post in blog_posts:
        if blog_post.id == id:
            return blog_post.dict()
    LOGGER.warning("Post não encontrado")
    raise HTTPException(status_code=404, detail="Post not found")

@app.delete("/service/blog/{id}")
async def delete_blog_post(id: int):
    global blog_posts
    blog_posts = [blog for blog in blog_posts if blog.id != id]
    return {"status": "sucesso"}

@app.put("/service/blog/{id}")
async def update_blog_post(id: int):
    global blog_posts
    for index, blog_post in enumerate(blog_posts):
        if blog_post.id == id:
            blog_posts[index] = BlogPost(**blog_post.dict(), **Request.json)
            return {"status": "sucesso"}
    LOGGER.warning("Post não encontrado")
    raise HTTPException(status_code=404, detail="Post not found")
