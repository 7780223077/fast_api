from pydantic import BaseModel, EmailStr
from datetime import datetime


#for posts
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class Post(PostBase):
    id: int
    created_at: datetime
    user_id: int
    # user: UserOut

    class Config:
        from_attributes = True

class PostWithVotes(BaseModel):
    Post : Post
    votes: int

    class Config:
        from_attributes = True


#for users
class UserBase(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    posts: list[Post]

    class Config:
        from_attributes = True


#for token
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: int | None = None
    # username: str | None = None

class VoteBase(BaseModel):
    post_id: int
    dir: int

class Student(BaseModel):
    pass


