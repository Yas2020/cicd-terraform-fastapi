from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import List

# declare your schema
class PostBase(BaseModel):
    title : str
    content : str
    published : bool = True


# To have more customized model schema for creating posts later if we want
class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    pass


class UserOut(BaseModel):
    email: str
    id: str

    class Config:
        orm_mode = True


class Post(PostBase):
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: str = None
    

class Vote(BaseModel):
    post_id: int
    dir: int
