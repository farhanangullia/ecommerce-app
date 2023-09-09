from typing import List, Optional

from pydantic import BaseModel


class Product(BaseModel):
    id: int
    name: str
    description: str
    price: float
    image: str


class CartItem(BaseModel):
    id: int
    name: str
    description: str
    price: float
    count: int


class Cart(BaseModel):
    items: Optional[List[CartItem]]
