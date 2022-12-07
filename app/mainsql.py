from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor

import os
import time
from dotenv import load_dotenv

# Create environment variables for the database.
load_dotenv(dotenv_path='.env')

FASTAPI_SERVER = os.getenv('FASTAPI_SERVER')
FASTAPI_DATABASE = os.getenv('FASTAPI_DATABASE')
FASTAPI_USER = os.getenv('FASTAPI_USER')
FASTAPI_PASSWORD = os.getenv('FASTAPI_PASSWORD')

# Instance of fastapi
app = FastAPI()


# Created a schema
class Post(BaseModel):
    title: str
    content: str
    published: bool = True


# Connection to the database
while True:

    try:
        conn = psycopg2.connect(host=FASTAPI_SERVER, database=FASTAPI_DATABASE,
                                user=FASTAPI_USER, password=FASTAPI_PASSWORD, cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successfull!")
        break
    except Exception as error:
        print("Connection to database failed")
        print('Error', error)
        time.sleep(2)


# Store posts objects
my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, {
    "title": "favorite foods", "content": "I like lamb barbacue", "id": 2}]


# Find the id
def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p


# Find the index
def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


# API requests
@app.get("/")
def root():
    return {"message": "Hello World!"}


@app.get('/posts')
def get_posts():
    cursor.execute(""" SELECT  * FROM posts """)
    posts = cursor.fetchall()
    print(posts)
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute(""" INSERT INTO posts (title, content, published) VALUES(%s, %s, %s) RETURNING * """,
                   (post.title, post.content, post.published))
    new_post = cursor.fetchone()

    conn.commit()

    return {"data": new_post}


@app.get('/posts/{id}')
def get_post(id: int):
    cursor.execute(""" SELECT * FROM posts WHERE id= %s """, (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")

    return {"post details": post}


# Delete post - status code in fastapi returns a response.
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute(
        """ DELETE FROM posts WHERE id= %s RETURNING * """, (str(id),))
    delete_post = cursor.fetchone()
    conn.commit()
    if delete_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist ")

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Update posts
@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """,
                   (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist ")

    return {"data": updated_post}
