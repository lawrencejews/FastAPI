from fastapi import FastAPI
from . import models
from .database import engine

from .routers import post, user, auth, vote

# Call to create table for the database
models.Base.metadata.create_all(bind=engine)

# Instance of fastapi
app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
