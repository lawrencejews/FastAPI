from pydantic import BaseModel, EmailStr
from datetime import datetime

# Created a schema from pydantic defines the structure
# This is for validation of data from the server.


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class PostResponse(PostBase):
    id: int
    created_at:  datetime 

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int 
    email: EmailStr 

    class Config:
        orm_mode = True
