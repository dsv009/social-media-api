from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, {"title":"favourite foods","content": "content of 2 post", "id":2}]
 
def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p['id'] == id:
            return i

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

while True:

    try:
        
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('database connection was successfull!')
        break
    except Exception as error:
        print('connecting to database failed')
        print('error was', error)
        time.sleep(2)




@app.get('/')
async def root():
    return {'message':'Hello world'}

@app.get('/posts')
def get_posts():
    cursor.execute('SELECT * FROM posts')
    posts = cursor.fetchall()
    return {'data': posts}

@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute('INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *',
    (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {'data': new_post}

@app.get('/posts/{id}')
def get_post(id: int):
    cursor.execute('SELECT * FROM posts WHERE id = %s', (str(id)))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f"post with id: {id} was not found"}
    print(post)
    return {'post_detail': post}

@app.delete('/posts/{id}', status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} does not exist')

    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put('/posts/{id}')
def update_post(id: int, post: Post):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} does not exist')
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {'data': post_dict}


