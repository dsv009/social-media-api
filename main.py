from typing import Optional
from fastapi import Body, FastAPI
from pydantic import BaseModel
from random import randrange

app = FastAPI()

my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, {"title":"favourite foods","content": "content of 2 post", "id":2}]
 
class Post(BaseModel):
    title: str
    content: str
    Published: bool = True
    rating: Optional[int] = None

@app.get('/')
async def root():
    return {'message':'Hello world'}

@app.get('/posts')
def get_posts():
    return {'data': my_posts}

@app.post('/posts')
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 100000000)
    my_posts.append(post_dict)
    return {'data': post_dict}
