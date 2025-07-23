from .. import models, schemas, oath2
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import func, or_
from ..database import get_db
from typing import List, Optional


router = APIRouter(
    prefix="/channels",
    tags=["Channels"]
)

print("Channels router loaded")

# GET all channels
@router.get("/", response_model=List[schemas.ChannelResponse])
def get_channels(db: Session = Depends(get_db), current_user: int = Depends(oath2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    q = db.query(models.Channel)

    if search:
        term = f"%{search}%"
        q = q.filter(models.Channel.name.ilike(term))

    channels = q.order_by(models.Channel.created_at.desc()).offset(skip).limit(limit).all()
    return channels

# GET ID specific channel
@router.get("/{id}", response_model=schemas.ChannelDetailResponse)
def get_channel(id: int, db: Session = Depends(get_db), current_user: int = Depends(oath2.get_current_user)):
    channel = db.query(models.Channel).filter(models.Channel.id == id).first()
    if not channel:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The channel with the id: {id} was not found")
    
    return channel

# POST a new channel
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ChannelResponse)
def create_channel(channel: schemas.ChannelCreate, db: Session = Depends(get_db), current_user: int = Depends(oath2.get_current_user)):
    new_channel = models.Channel(**channel.model_dump())
    db.add(new_channel)
    db.commit()
    db.refresh(new_channel)
    return new_channel