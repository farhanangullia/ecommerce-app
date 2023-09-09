from typing import List, Optional

from app.adapters.models import pgsql_model
from app.domain.model.checkout import Order
from app.domain.ports.repository import OrderRepository
from sqlmodel import Session, select


class PgsqlOrderRepository(OrderRepository):
    def __init__(self, engine) -> None:
        self.__engine = engine

    def create_order(self, order: Order) -> None:
        with Session(self.__engine) as session:
            session.add(pgsql_model.Order(**order.dict()))
            session.commit()

    def list_orders(self) -> List[Order]:
        with Session(self.__engine) as session:
            statement = select(pgsql_model.Order)

            results = session.exec(statement)
            orders = results.all()

        return orders

    def list_orders_by_customer(self, customer_id: str) -> List[Order]:
        with Session(self.__engine) as session:
            statement = select(pgsql_model.Order)
            statement = (
                select(pgsql_model.Order)
                .where(pgsql_model.Order.customer_id == customer_id)
                .order_by(pgsql_model.Order.created_on.desc())
            )

            results = session.exec(statement)
            orders = results.all()

        return orders

    def get_order(self, id: str) -> Optional[Order]:
        with Session(self.__engine) as session:
            order = session.get(pgsql_model.Order, id)
        return order
