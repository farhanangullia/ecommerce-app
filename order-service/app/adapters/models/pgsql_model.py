from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlmodel import Field, SQLModel


class Order(SQLModel, table=True):
    __tablename__ = "orders"

    id: Optional[UUID] = Field(default=None, primary_key=True)
    created_on: datetime
    customer_id: str
    total_amount: float
