import datetime
from sqlmodel import Field, SQLModel
from sqlalchemy import TIMESTAMP, Column, Boolean, String, text, true

class Post(SQLModel, table=True):
    __tablename__ = "posts" # type: ignore

    id: int = Field(default=None, primary_key=True)
    title: str = Field(sa_column=Column(String, nullable=False))
    content: str = Field(sa_column=Column(String, nullable=False))
    published: bool = Field(sa_column=Column(Boolean, nullable=False, server_default="true"))
    created_at: datetime.datetime = Field(sa_column=Column(TIMESTAMP (timezone=True), nullable=False, server_default=text("now()")))
