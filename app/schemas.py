from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

from app.database import Base


class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse
    
    class Config:
        orm_mode = True

class PostVoteResponse(BaseModel):
    post: PostResponse
    likes: int = 0  # Default to 0 if no votes are found

    class Config: # type: ignore
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

# Change this if you want to include more data in the token
class TokenData(BaseModel):
    id: Optional[int] = None

    class Config:
        orm_mode = True

class Vote(BaseModel):
    post_id: int
    direction: bool # True for upvote, False for downvote

    class Config:
        orm_mode = True