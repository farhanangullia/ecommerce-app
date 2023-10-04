from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel, Field


class ShippingDetails(BaseModel):
    address: str = Field(min_length=1)
    country: str = Field(min_length=1)


class CheckoutRequest(BaseModel):
    shipping_details: ShippingDetails = Field(alias="shippingDetails")


class CheckoutResponse(BaseModel):
    order_id: str
    created_on: datetime
    total_amount: float
    shipping_tracking_id: str


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
