from typing import List

from pydantic import BaseModel


class Product(BaseModel):
    id: int
    name: str
    description: str
    price: float
    image: str


class GetProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float
    image: str


class GetProductsResponse(BaseModel):
    products: List[Product]
