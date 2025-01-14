from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field


class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"


class User(BaseModel):
    id: int
    email: EmailStr
    username: str
    hashed_password: str
    role: UserRole = UserRole.USER


class OrderStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class Product(BaseModel):
    id: int
    name: str
    description: str
    price: float = Field(gt=0)  # Price must be greater than 0


class OrderItem(BaseModel):
    order_id: int
    product_id: int
    quantity: int = Field(gt=0)
    unit_price: float = Field(gt=0)  # Price at time of order
    subtotal: float = Field(gt=0)


class Item(BaseModel):
    # Define fields for Item
    id: int
    quantity: int
    # Add other fields as necessary


class Order(BaseModel):
    id: int
    user_id: int
    items: List[Item]  # Ensure this field is defined and is a list of Item
    total_price: float = Field(gt=0)
    status: OrderStatus
    created_at: datetime
    updated_at: Optional[datetime] = None
    products: Optional[List[Product]] = None
