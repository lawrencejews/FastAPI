from fastapi import FastAPI,  Response, status, HTTPException, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from . import models, schemas
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


# The root path to sqlalchemy
@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):

    posts = db.query(models.Post).all()
    return {"data": posts}


# Get all post from postgres
@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):

    posts = db.query(models.Post).all()
    return {"data": posts}


# Create a post in postgres
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: schemas.Post, db: Session = Depends(get_db)):

    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}


# Get a post id from postgres
@app.get('/posts/{id}')
def get_post(id: int, db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")

    return {"post details": post}


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
@app.put("/posts/{id}")
def update_post(id: int, updated_post: schemas.Post, db: Session = Depends(get_db)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist ")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return {"data": post}
