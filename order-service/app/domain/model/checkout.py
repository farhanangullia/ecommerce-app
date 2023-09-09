from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


class Product(BaseModel):
    id: int
    name: str
    description: str
    price: float
    image: str


class Order(BaseModel):
    id: UUID
    created_on: datetime
    customer_id: str
    total_amount: float


class CartItem(BaseModel):
    id: int
    name: str
    description: str
    price: float
    count: int


class Cart(BaseModel):
    items: Optional[List[CartItem]]
