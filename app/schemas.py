from pydantic import BaseModel


# Created a schema from pydantic defines the structure
# This is for validation of data from the server.
class Post(BaseModel):
    title: str
    content: str
    published: bool = True


class CreatePost(BaseModel):
    title: str
    content: str
    published: bool = True


class UpdatePost(BaseModel):
    title: str
    content: str
    published: bool
