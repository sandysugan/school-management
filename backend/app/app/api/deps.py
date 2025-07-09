from typing import Generator
from app.core.config import settings
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.models import Apitoken, User
from app.db.session import SessionLocal

# reusable_oauth2 = OAuth2PasswordBearer(
#     tokenUrl=f"{settings.API_V1_STR}/login/access-token")

"""Initializing the database Connection"""
def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
        
def get_current_user(token: str, db: Session = Depends(get_db)):
    token_obj = db.query(Apitoken).filter(
        Apitoken.token == token,
        Apitoken.status == 1
    ).first()

    if not token_obj:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    user = db.query(User).filter(User.id == token_obj.user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user

