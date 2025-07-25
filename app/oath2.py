from fastapi import Depends
from fastapi.security import OAuth2, OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import os
from app.config import settings

OAuth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.secret_key  # type: ignore
ALGORITHM = settings.algorithm  # type: ignore
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes  # type: ignore
def create_access_token(data: dict):
    to_encode = data.copy()
    
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM) # type: ignore

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:    
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) # type: ignore
        id: str = payload.get("user_id") # type: ignore
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)  # type: ignore
    except JWTError:
        raise credentials_exception
    
    # Token data currently only contains user_id, but you can expand it to include more data if needed
    return token_data
    
def get_current_user(token: str = Depends(OAuth2_scheme), db: Session =Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token = verify_access_token(token, credentials_exception) # type: ignore
    user = db.query(models.User).filter(models.User.id == token.id).first()  # type: ignore
    if not user:
        raise credentials_exception
    return user  # type: ignore