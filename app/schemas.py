from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional

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

class ChannelBase(BaseModel):
    name: str


class ChannelCreate(ChannelBase):
    name: str
    description: str

    class Config:
        orm_mode = True

class ChannelResponse(ChannelBase):
    id: int

    class Config:
        orm_mode = True


class ChannelDetailResponse(ChannelResponse):
    description: str
    posts: List['PostSummaryResponse'] = []


    class Config: # type: ignore
        orm_mode = True


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    channel_ids: List[int]

class Reply(BaseModel):
    content: str

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

class PostSummaryResponse(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    created_at: datetime
    owner: UserResponse
    channels: List[ChannelResponse] # List of channels associated with the post

    likes: int = 0  # Default to 0 if no votes are found
    direct_reply_count: int
    total_reply_count: int

    class Config:
        orm_mode = True

class PostDetailResponse(PostSummaryResponse):
   
    replies: Optional[List[PostSummaryResponse]] = None  # List of replies if any

    class Config: # type: ignore
        pass

PostDetailResponse.update_forward_refs()  # Update forward references for nested models

class Token(BaseModel):
    access_token: str
    token_type: str

# Change this if you want to include more data in the token
class TokenData(BaseModel):
    id: Optional[int] = None

    class Config:
        orm_mode = True

class Vote(BaseModel):
    direction: bool # True for upvote, False for downvote

    class Config:
        orm_mode = True

ChannelDetailResponse.update_forward_refs()
PostDetailResponse.update_forward_refs()
