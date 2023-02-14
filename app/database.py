from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
import time
from .config import settings


# Instance of creating a database
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ===============================================================================================
#    This code below can be used to connect to the database if you choose not to use SQLALCHEMY
# ================================================================================================

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
