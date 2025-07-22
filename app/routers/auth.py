from os import access
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import func
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas, utils, oath2

router = APIRouter(tags=["Authentication"])

print("Auth router loaded")

@router.post("/login", response_model=schemas.Token)  # type: ignore
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first() # type: ignore

    # Check if user exists
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid credentials")
    
    # Verify password with the found User password
    if not utils.verify_password(user_credentials.password, user.password):  # type: ignore
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

    # Check if badge points align during login
    badge_count = (
    db.query(func.count(models.Vote.id))
    .filter(models.Vote.user_id == user.id, models.Vote.like_by_owner == True)
    .scalar()
    )

    if user.badge_points != badge_count:
        user.badge_points = badge_count
        db.commit()

    
    # Create access token
    # You choose what data you want to include in the token
    # Here we include the user ID, but you can include more or different data if needed
    access_token = oath2.create_access_token(data={"user_id": user.id})  # type: ignore


    return {"access_token": access_token, "token_type": "bearer"}  # type: ignore