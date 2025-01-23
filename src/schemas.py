from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field

from .models import OrderStatus, UserRole


class UserBase(BaseModel):
    email: EmailStr
    username: str


class UserCreate(UserBase):
    password: str


class UserInDB(UserBase):
    id: int
    role: UserRole
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[UserRole] = None


class ProductBase(BaseModel):
    name: str
    description: str
    price: float = Field(gt=0)


class ProductCreate(ProductBase):
    pass


class ProductResponse(ProductBase):
    id: int


class OrderItem(BaseModel):
    id: int
    quantity: int = Field(gt=0)  # Ensure quantity is greater than 0


class OrderBase(BaseModel):
    items: List[OrderItem]  # Changed from single product to list of items


class OrderCreate(OrderBase):
    pass


class OrderResponse(BaseModel):
    id: int
    user_id: int
    items: List[OrderItem]
    total_price: float
    status: OrderStatus
    created_at: datetime
    updated_at: Optional[datetime] = None
    delivery_date: Optional[datetime] = None
    products: Optional[List[ProductResponse]] = None
