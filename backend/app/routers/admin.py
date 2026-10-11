from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session, joinedload
from ..database import get_db
from ..models import Product, Order
from ..schemas import ProductIn, StatusIn
from ..deps import admin_user
from .products import product_out
from .orders import order_out
router=APIRouter(prefix="/admin",tags=["admin"],dependencies=[Depends(admin_user)])
@router.post("/products",status_code=201)
def create_product(data:ProductIn,db:Session=Depends(get_db)):
    p=Product(**data.model_dump());db.add(p);db.commit();db.refresh(p);return product_out(p)
@router.put("/products/{product_id}")
def update_product(product_id:int,data:ProductIn,db:Session=Depends(get_db)):
    p=db.query(Product).filter(Product.id==product_id).first()
    if not p: raise HTTPException(status_code=404,detail="Product not found")
    for k,v in data.model_dump().items(): setattr(p,k,v)
    db.commit();db.refresh(p);return product_out(p)
@router.delete("/products/{product_id}",status_code=204)
def delete_product(product_id:int,db:Session=Depends(get_db)):
    p=db.query(Product).filter(Product.id==product_id).first()
    if not p: raise HTTPException(status_code=404,detail="Product not found")
    p.is_active=False;db.commit();return Response(status_code=204)
@router.get("/orders")
def all_orders(db:Session=Depends(get_db)):
    orders=db.query(Order).options(joinedload(Order.items)).order_by(Order.created_at.desc()).limit(300).all()
    return {"items":[order_out(o) for o in orders]}
@router.patch("/orders/{order_id}")
def update_order(order_id:int,data:StatusIn,db:Session=Depends(get_db)):
    allowed={"Placed","Processing","Shipped","Delivered","Cancelled"}
    if data.status not in allowed: raise HTTPException(status_code=422,detail="Unsupported order status")
    o=db.query(Order).filter(Order.id==order_id).first()
    if not o: raise HTTPException(status_code=404,detail="Order not found")
    o.status=data.status;db.commit();db.refresh(o);return {"id":o.id,"status":o.status}
