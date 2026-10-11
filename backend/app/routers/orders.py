from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from ..database import get_db
from ..models import User, Product, Order, OrderItem
from ..schemas import CheckoutIn
from ..deps import current_user
router=APIRouter(prefix="/orders",tags=["orders"])
def order_out(o:Order): return {"id":o.id,"user_id":o.user_id,"customer_name":o.customer_name,"customer_email":o.customer_email,"customer_phone":o.customer_phone,"customer_address":o.customer_address,"total":o.total,"status":o.status,"created_at":o.created_at.isoformat() if o.created_at else "","items":[{"id":i.id,"product_id":i.product_id,"product_name":i.product_name,"unit_price":i.unit_price,"quantity":i.quantity,"image":i.image} for i in o.items]}
@router.post("",status_code=201)
def create_order(data:CheckoutIn,db:Session=Depends(get_db),user:User=Depends(current_user)):
    try:
        lines=[];total=0.0
        for item in data.items:
            product=db.query(Product).filter(Product.id==item.product_id,Product.is_active==True).with_for_update().first()
            if not product: raise HTTPException(status_code=404,detail=f"Product {item.product_id} was not found")
            if product.stock<item.quantity: raise HTTPException(status_code=409,detail=f"Not enough stock for {product.name}")
            product.stock-=item.quantity; total+=product.price*item.quantity
            lines.append((product,item.quantity))
        order=Order(user_id=user.id,customer_name=data.customer_name.strip(),customer_email=user.email,customer_phone=data.customer_phone.strip(),customer_address=data.customer_address.strip(),total=round(total,2),status="Placed")
        db.add(order);db.flush()
        for product,qty in lines: db.add(OrderItem(order_id=order.id,product_id=product.id,product_name=product.name,unit_price=product.price,quantity=qty,image=product.image))
        db.commit();db.refresh(order)
        return {"id":order.id,"status":order.status,"total":order.total,"message":"Order placed successfully"}
    except Exception:
        db.rollback();raise
@router.get("/me")
def my_orders(db:Session=Depends(get_db),user:User=Depends(current_user)):
    orders=db.query(Order).options(joinedload(Order.items)).filter(Order.user_id==user.id).order_by(Order.created_at.desc()).all()
    return {"items":[order_out(o) for o in orders]}
