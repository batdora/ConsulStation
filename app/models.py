from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, TIMESTAMP, text
from sqlalchemy.orm import relationship

from app.routers import vote
from .database import Base

print("Models loaded")

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default="true", nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    reply_to = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=True)  # Allow None for root posts
    original_post_owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)  # Owner of the original post
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    direct_reply_count = Column(Integer, nullable=False, default=0)
    total_reply_count  = Column(Integer, nullable=False, default=0)
    likes = Column(Integer, nullable=False, default=0)  # Default to 0 if no votes are found
    
    # Relationships
    owner = relationship("User", foreign_keys= [owner_id], back_populates="posts")
    original_post_owner = relationship("User", foreign_keys=[original_post_owner_id], back_populates="original_posts")

    parent   = relationship("Post",remote_side=[id],back_populates="replies")
    replies  = relationship("Post",back_populates="parent",cascade="all, delete-orphan")
    votes = relationship("Vote", back_populates="post", cascade="all, delete-orphan")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))

    # Relationships
    posts = relationship("Post", foreign_keys="[Post.owner_id]", back_populates="owner")
    original_posts = relationship("Post", foreign_keys="[Post.original_post_owner_id]", back_populates="original_post_owner")
    votes = relationship("Vote", back_populates="user", cascade="all, delete-orphan")

class Vote(Base):
    __tablename__ = "votes"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    like_by_owner = Column(Boolean, default=False)  # Indicates if the post owner liked their own post
    
    # Relationships
    user = relationship("User")
    post = relationship("Post")