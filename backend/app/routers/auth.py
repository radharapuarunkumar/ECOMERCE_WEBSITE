from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
from ..schemas import RegisterIn, LoginIn, TokenOut, UserOut
from ..security import hash_password, verify_password, create_access_token
from ..deps import current_user
router=APIRouter(prefix="/auth",tags=["authentication"])
@router.post("/register",response_model=TokenOut,status_code=201)
def register(data:RegisterIn,db:Session=Depends(get_db)):
    email=data.email.lower().strip()
    if db.query(User).filter(User.email==email).first(): raise HTTPException(status_code=409,detail="An account with this email already exists.")
    user=User(name=data.name.strip(),email=email,password_hash=hash_password(data.password),role="customer")
    db.add(user);db.commit();db.refresh(user)
    return {"access_token":create_access_token(str(user.id)),"user":user}
@router.post("/login",response_model=TokenOut)
def login(data:LoginIn,db:Session=Depends(get_db)):
    user=db.query(User).filter(User.email==data.email.lower().strip()).first()
    if not user or not verify_password(data.password,user.password_hash): raise HTTPException(status_code=401,detail="Incorrect email or password.")
    if not user.is_active: raise HTTPException(status_code=403,detail="This account is disabled.")
    return {"access_token":create_access_token(str(user.id)),"user":user}
@router.get("/me",response_model=UserOut)
def me(user:User=Depends(current_user)): return user
