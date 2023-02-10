from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# Created a schema from pydantic defines the structure
# This is for validation of data from the server [I/O].
class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


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
    owner_id: int 
    owner: UserOut

    class Config:
        orm_mode = True
