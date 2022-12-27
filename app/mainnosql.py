from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models
from .database import engine

import os
import time
from dotenv import load_dotenv

from .routers import post, user, auth


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


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
