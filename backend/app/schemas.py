from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
class RegisterIn(BaseModel): name: str = Field(min_length=2,max_length=120); email: EmailStr; password: str = Field(min_length=8,max_length=128)
class LoginIn(BaseModel): email: EmailStr; password: str = Field(min_length=1,max_length=128)
class UserOut(BaseModel): id:int; name:str; email:EmailStr; role:str; model_config=ConfigDict(from_attributes=True)
class TokenOut(BaseModel): access_token:str; token_type:str="bearer"; user:UserOut
class ProductIn(BaseModel): name:str=Field(min_length=2,max_length=200); category:str=Field(default="General",max_length=100); price:float=Field(ge=0); old_price:float=Field(default=0,ge=0); rating:float=Field(default=4.5,ge=0,le=5); image:str=""; description:str=""; stock:int=Field(default=0,ge=0); badge:str="FEATURED"
class ProductOut(ProductIn): id:int; created_at:str=""; model_config=ConfigDict(from_attributes=True)
class CheckoutItem(BaseModel): product_id:int; quantity:int=Field(ge=1,le=20)
class CheckoutIn(BaseModel): customer_name:str=Field(min_length=2,max_length=120); customer_phone:str=Field(min_length=7,max_length=30); customer_address:str=Field(min_length=8,max_length=1000); items:list[CheckoutItem]=Field(min_length=1,max_length=30)
class StatusIn(BaseModel): status:str
