from typing import List, Optional

from pydantic import BaseModel


class CartItem(BaseModel):
    id: int
    name: str
    description: str
    price: float
    count: int


class GetCartResponse(BaseModel):
    items: Optional[List[CartItem]]


class AddToCartRequest(BaseModel):
    id: int
    name: str
    description: str
    price: float
    image: str
