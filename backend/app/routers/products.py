from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from ..database import get_db
from ..models import Product
router=APIRouter(prefix="/products",tags=["products"])
def product_out(p:Product): return {"id":p.id,"name":p.name,"category":p.category,"price":p.price,"old_price":p.old_price,"rating":p.rating,"image":p.image,"description":p.description,"stock":p.stock,"badge":p.badge,"created_at":p.created_at.isoformat() if p.created_at else ""}
@router.get("")
def list_products(category:str|None=None,search:str|None=None,limit:int=Query(default=100,ge=1,le=200),offset:int=Query(default=0,ge=0),db:Session=Depends(get_db)):
    q=db.query(Product).filter(Product.is_active==True)
    if category and category!="All": q=q.filter(Product.category==category)
    if search: q=q.filter(or_(Product.name.ilike(f"%{search}%"),Product.category.ilike(f"%{search}%"),Product.description.ilike(f"%{search}%")))
    total=q.count(); items=q.order_by(Product.created_at.desc(),Product.id.desc()).offset(offset).limit(limit).all()
    return {"items":[product_out(p) for p in items],"total":total,"limit":limit,"offset":offset}
@router.get("/{product_id}")
def get_product(product_id:int,db:Session=Depends(get_db)):
    p=db.query(Product).filter(Product.id==product_id,Product.is_active==True).first()
    if not p: raise HTTPException(status_code=404,detail="Product not found")
    return product_out(p)
