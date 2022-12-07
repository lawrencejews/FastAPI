from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import time
from dotenv import load_dotenv

# Create environment variables for the database.
load_dotenv(dotenv_path='.env')

user = os.getenv('FASTAPI_USER')
password = os.getenv('FASTAPI_PASSWORD')
postgresserver = os.getenv('FASTAPI_SERVER')
db = os.getenv('FASTAPI_DATABASE')


# Instance of creating a database
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:lubs@localhost:5432/fastapi'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
