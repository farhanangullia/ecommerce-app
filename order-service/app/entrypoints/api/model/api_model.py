from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel


class CheckoutResponse(BaseModel):
    order_id: str
    created_on: datetime
    total_amount: float


class Order(BaseModel):
    id: UUID
    created_on: datetime
    customer_id: str
    total_amount: float


class GetOrderResponse(BaseModel):
    id: UUID
    created_on: datetime
    customer_id: str
    total_amount: float


class GetOrdersResponse(BaseModel):
    orders: List[Order]
