from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .database import get_db
from .models import User
from .security import decode_token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
def current_user(token:str=Depends(oauth2_scheme), db:Session=Depends(get_db))->User:
    payload=decode_token(token); sub=payload.get("sub") if payload else None
    if not sub: raise HTTPException(status_code=401,detail="Invalid or expired login. Please sign in again.",headers={"WWW-Authenticate":"Bearer"})
    user=db.query(User).filter(User.id==int(sub),User.is_active==True).first()
    if not user: raise HTTPException(status_code=401,detail="User account not found or disabled.")
    return user
def admin_user(user:User=Depends(current_user))->User:
    if user.role!="admin": raise HTTPException(status_code=403,detail="Admin access required.")
    return user
