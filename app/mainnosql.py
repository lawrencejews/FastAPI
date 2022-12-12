from typing import List
from fastapi import FastAPI,  Response, status, HTTPException, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session

from . import models, schemas

from . import models
from . import models
from .database import engine, get_db
import os
import time
from dotenv import load_dotenv


# Call to create table for the database
models.Base.metadata.create_all(bind=engine)


# Instance of fastapi
app = FastAPI()


# Create environment variables for the database.
load_dotenv(dotenv_path='.env')

FASTAPI_SERVER = os.getenv('FASTAPI_SERVER')
FASTAPI_DATABASE = os.getenv('FASTAPI_DATABASE')
FASTAPI_USER = os.getenv('FASTAPI_USER')
FASTAPI_PASSWORD = os.getenv('FASTAPI_PASSWORD')


# Connection to the database
while True:

    try:
        conn = psycopg2.connect(host=FASTAPI_SERVER,
                                database=FASTAPI_DATABASE,
                                user=FASTAPI_USER,
                                password=FASTAPI_PASSWORD,
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successfull!")
        break
    except Exception as error:
        print("Connection to database failed")
        print('Error', error)
        time.sleep(2)


# ======================POSTS TABLE===========================================================
# Get all post from postgres
@app.get("/posts", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):

    posts = db.query(models.Post).all()
    return posts


# Create a post in postgres
@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):

    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


# Get a post id from postgres
@app.get('/posts/{id}',  response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")

    return post


# Delete post - status code in fastapi returns a response.
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist ")

    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Update posts
@app.put("/posts/{id}", response_model=schemas.PostResponse)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist ")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()


# =========================USERS TABLE=======================================================
@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
